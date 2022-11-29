import csv
import json
import pprint
import unicodedata
import xmlschema
from collections import defaultdict
from datetime import datetime
from loguru import logger
from lxml import etree
from suds.cache import FileCache
from suds.client import Client
from suds.sax.text import Raw
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.formats.dataclass.serializers.xml import XmlSerializer
from xsdata.models.datatype import XmlDate


from . import core, token, utils
from .leiautes import *
from .leiautes.com.xsd.lote_eventos.envio.envio_lote_eventos_v1_1_1 import *
from transports import HttpTransportSuds

CNPJ8 = "29138393"
CNPJ11 = "29138393000186"

TIPO_AMBIENTE: tipos.TipoAmbiente = tipos.TipoAmbiente.PRODUCAO
PROCESSO_EMISSAO: tipos.TsProcEmiSem8 = tipos.TsProcEmiSem8.VALUE_1
VERSAO_APLICATIVO = '0.1'

if core.TIPO_AMBIENTE == utils.TipoAmbiente.PRODUCAO:
    URL_RAIZ_ENVIO = 'https://webservices.envio.esocial.gov.br'
    URL_RAIZ_CONSULTA = 'https://webservices.consulta.esocial.gov.br'
else:
    URL_RAIZ_ENVIO = 'https://webservices.producaorestrita.esocial.gov.br'
    URL_RAIZ_CONSULTA = URL_RAIZ_ENVIO

URL_CONSULTA = f'{URL_RAIZ_CONSULTA}/servicos/empregador/consultarloteeventos/WsConsultarLoteEventos.svc?singleWsdl'
URL_ENVIO = f'{URL_RAIZ_ENVIO}/servicos/empregador/enviarloteeventos/WsEnviarLoteEventos.svc?singleWsdl'

transport = HttpTransportSuds()
transport.urlopener = token.opener

cache = FileCache(location=core.DIR_APLICATION.joinpath('cache'), days=1)
cache.remove_default_location_on_exit = False

serializer_config = SerializerConfig(
    xml_declaration=False,
)
xml_serializer = XmlSerializer(config=serializer_config)

IDE_EMPREGADOR = {
    'tp_insc': utils.TipoIncricao.CNPJ,
    'nr_insc': CNPJ8,
}

IDE_TRANSMISSOR = {
    'tp_insc': utils.TipoIncricao.CNPJ,
    'nr_insc': CNPJ11,
}

identificadores = defaultdict(int)

def gerar_id():
    id_parcial = f"ID1{CNPJ8:<014}{datetime.now().strftime('%Y%m%d%H%M%S')}"
    sequencia = identificadores[id_parcial] + 1
    identificadores[id_parcial] = sequencia
    return f"ID1{CNPJ8:<014}{datetime.now().strftime('%Y%m%d%H%M%S')}{sequencia:>05}"

def envio_lote_eventos(evs: dict, grupo: utils.LoteEventosTipoGrupo) -> str:
    lista_eventos_assinados = defaultdict()
    for id_, ev in evs.items():
        ns_map = {None: ev.__class__.Meta.namespace}
        xml_s1000 = XmlSerializer().render(obj=ev, ns_map=ns_map)
        xml_signer = token.assinar(xml=xml_s1000)
        xml_string = etree.tostring(xml_signer)

        schema = xmlschema.XMLSchema(ev.__class__.Meta.schema)
        if not schema.is_valid(xml_string):
            schema.validate(xml_string)
        else:
            lista_eventos_assinados[id_] = xml_signer

    eventos = ESocial.EnvioLoteEventos.Eventos(
        evento=None,
    )
    ide_empregador = TideEmpregador(
        **IDE_EMPREGADOR
    )
    ide_transmissor = TideTransmissor(
        **IDE_TRANSMISSOR
    )
    envio_lote_eventos = ESocial.EnvioLoteEventos(
        ide_empregador=ide_empregador,
        ide_transmissor=ide_transmissor,
        eventos=eventos,
        grupo=grupo,
    )
    esocial = ESocial(
        envio_lote_eventos=envio_lote_eventos
    )
    ns_map_envio_lote_eventos = {None: ESocial.Meta.namespace}
    xml_esocial = xml_serializer.render(
        obj=esocial,
        ns_map=ns_map_envio_lote_eventos
    )

    xml_parser = etree.XMLParser(remove_blank_text=True)
    xml_envio_lote_eventos = etree.fromstring(xml_esocial, xml_parser)
    eventos = xml_envio_lote_eventos.find(".//eventos", ns_map_envio_lote_eventos)
    eventos_items = {}
    for id_, ev in lista_eventos_assinados.items():
        eventos_items[id_] = etree.SubElement(eventos, 'evento', Id=id_)
        eventos_items[id_].append(ev)

    xml_esocial = etree.tostring(xml_envio_lote_eventos)
    with open('test_envio_lote_eventos.xml', 'wb') as arq:
        arq.write(xml_esocial)

    return xml_esocial.decode()

def montar_S1200(ind_retif: tipos.TsIndRetif, per_apur: str, identificador: str, cod_categ: str,
        cnpj_est: str, cbo: str, cpf_trab: str, cod_lotacao: str, nome:str, dt_nasc: str,
        remuneracoes: List[S1200.TItensRemun], nr_recibo: Optional[str]=None, anual: bool=False,
        matricula: Optional[str]=None
    ) -> str:
    ide_evento = tipos.TIdeEventoFolha(
        ind_retif=ind_retif,
        nr_recibo=nr_recibo,
        ind_apuracao=tipos.TsIndApuracao.VALUE_2 if anual else tipos.TsIndApuracao.VALUE_1,
        per_apur=per_apur,
        tp_amb=TIPO_AMBIENTE,
        proc_emi=PROCESSO_EMISSAO,
        ver_proc=VERSAO_APLICATIVO,
    )
    remun_per_apur = S1200.Evento.EvtRemun.DmDev.InfoPerApur.IdeEstabLot.RemunPerApur(
        matricula=matricula,
        itens_remun=remuneracoes,
    )
    ide_estab_lot = S1200.Evento.EvtRemun.DmDev.InfoPerApur.IdeEstabLot(
        tp_insc=tipos.TsTpInsc1.VALUE_1,
        nr_insc=cnpj_est,
        cod_lotacao=cod_lotacao,
        remun_per_apur=[remun_per_apur]
    )
    info_per_apur = S1200.Evento.EvtRemun.DmDev.InfoPerApur(
        ide_estab_lot=[ide_estab_lot]
    )
    info_compl_cont = S1200.Evento.EvtRemun.DmDev.InfoComplCont(
        cod_cbo=cbo,
    )
    dm_dev = S1200.Evento.EvtRemun.DmDev(
        ide_dm_dev=identificador,
        cod_categ=cod_categ,
        info_per_apur=info_per_apur,
        info_compl_cont=info_compl_cont,
    )
    info_complem = S1200.Evento.EvtRemun.IdeTrabalhador.InfoComplem(
        nm_trab=nome,
        dt_nascto=dt_nasc,
    )
    ide_trabalhador = S1200.Evento.EvtRemun.IdeTrabalhador(
        cpf_trab=cpf_trab,
        info_complem=info_complem,
    )
    id_ = gerar_id()
    ide_empregador = tipos.TIdeEmpregador(
        **IDE_EMPREGADOR
    )
    evt_remun = S1200.Evento.EvtRemun(
        ide_evento=ide_evento,
        ide_empregador=ide_empregador,
        ide_trabalhador=ide_trabalhador,
        dm_dev=dm_dev,
        id=id_
    )
    return id_, S1200.Evento(evt_remun=evt_remun)

def montar_S1210(cpf_benef: str, per_ref: str, pagamentos=List[S1210.Evento.EvtPgtos.IdeBenef.InfoPgto]):
    ide_evento = tipos.TIdeEventoFolha(
        ind_retif=tipos.TsIndRetif.VALUE_1,
        per_apur=per_ref,
        tp_amb=TIPO_AMBIENTE,
        proc_emi=PROCESSO_EMISSAO,
        ver_proc=VERSAO_APLICATIVO
    )
    ide_empregador = tipos.TIdeEmpregador(
        **IDE_EMPREGADOR
    )
    ide_benef = S1210.Evento.EvtPgtos.IdeBenef(
        cpf_benef=cpf_benef,
        info_pgto=pagamentos,
    )
    id_ = gerar_id()
    evt_pgtos = S1210.Evento.EvtPgtos(
        ide_evento=ide_evento,
        ide_empregador=ide_empregador,
        ide_benef=ide_benef,
        id=id_,
    )
    return id_, S1210.Evento(evt_pgtos=evt_pgtos)

def montar_S1210_Pagamento(dt_pgto: XmlDate, tp_pgto: S1210.InfoPgtoTpPgto, per_ref: str, dm_dev: str, valor: float):
    return S1210.Evento.EvtPgtos.IdeBenef.InfoPgto(
        dt_pgto=dt_pgto,
        tp_pgto=tp_pgto,
        per_ref=per_ref,
        ide_dm_dev=dm_dev,
        vr_liq=valor,
    )

def enviar_s1200(registros):
    arq = open(arquivo)
    arq_csv = csv.DictReader(arq, delimiter=';')
    recibos = []
    registros = defaultdict(dict)
    logger.info("Configurando eventos.")
    identificadores = {}
    for reg in arq_csv:
        registros[reg['CPF']] = reg
        if reg['ID S-1200'] != '' and reg['S-1200 Erro'] == '':
            continue
        remuneracao = S1200.TItensRemun(
            cod_rubr='REMUNERACAO',
            ide_tab_rubr='RPA',
            vr_rubr=utils.txt_para_num(reg['Valor']),
            ind_apur_ir='0',
        )
        inss = S1200.TItensRemun(
            cod_rubr='INSS',
            ide_tab_rubr='RPA',
            vr_rubr=utils.txt_para_num(reg['Dsc. INSS']),
            ind_apur_ir='0',
        )
        irrf = S1200.TItensRemun(
            cod_rubr='IRRF',
            ide_tab_rubr='RPA',
            vr_rubr=utils.txt_para_num(reg['Dsc. IRRF']),
            ind_apur_ir='0',
        )
        iss = S1200.TItensRemun(
            cod_rubr='ISSQN',
            ide_tab_rubr='RPA',
            vr_rubr=utils.txt_para_num(reg['Dsc. ISS']),
            ind_apur_ir='0',
        )
        dia, mes, ano = reg['Data de nascimento'].split('/')
        dt_nasc = XmlDate(
            year=int(ano),
            month=int(mes),
            day=int(dia),
        )
        dia, mes, ano = reg['Data do pagamento'].split('/')
        remuneracoes = [remuneracao, inss]
        if reg['Dsc. IRRF'] != '0':
            remuneracoes.append(irrf)
        if reg['Dsc. ISS'] != '0':
            remuneracoes.append(iss)
        
        nome = unicodedata.normalize(
            "NFKD", reg['Nome']
        ).encode(
            'ASCII', 'ignore'
        ).decode().upper().strip()
        id_, evento = montar_S1200(
            ind_retif=tipos.TsIndRetif.VALUE_1,
            per_apur=f'{ano}-{mes}',
            identificador='001',
            cod_categ=701,
            cnpj_est=CNPJ11,
            cbo='{0:>06}'.format(utils.limpar_doc(reg['CBO'])),
            cpf_trab='{0:>011}'.format(utils.limpar_doc(reg['CPF'])),
            cod_lotacao='001',
            nome=nome,
            dt_nasc=dt_nasc,
            remuneracoes=remuneracoes
        )
        recibos.append((id_, evento))
        registros[reg['CPF']]['Nome'] = nome
        registros[reg['CPF']]['ID S-1200'] = id_
        identificadores[id_] = reg['CPF']

    logger.info("Separando eventos em lotes.")
    lote_recibos = []
    while len(recibos) > 50:
        lote_recibos.append(recibos[:50])
        recibos = recibos[50:]
    lote_recibos.append(recibos)

    client = Client(URL_ENVIO, transport=transport)
    client.set_options(cache=cache)
    logger.info("Enviando os lotes.")
    for lote in lote_recibos:
        lote_dct = dict(lote)
        lote_para_envio = envio_lote_eventos(evs=lote_dct, grupo=utils.LoteEventosTipoGrupo.EVENTOS_PERIODICOS)
        result = client.service.EnviarLoteEventos(loteEventos=Raw(lote_para_envio))
        protocolo_envio = core.salvar_retorno(result) or ''
        logger.info("Lote enviado.")
        for evento in lote:
            cpf = identificadores[evento[0]]
            registros[cpf].update({
                'Protocolo de envio S-1200': protocolo_envio,
            })
    registros = list(registros.values())
    arq.close()
    if registros:
        arq2 = open(arquivo, 'w', newline='\n')
        arq2_csv = csv.DictWriter(arq2, fieldnames=list(registros[0].keys()), delimiter=';')
        arq2_csv.writeheader()
        arq2_csv.writerows(registros)

def consultar_s1200():
    arq = open(arquivo)
    arq_csv = csv.DictReader(arq, delimiter=';')
    registros = defaultdict(dict)
    for reg in arq_csv:
        registros[reg['Protocolo de envio S-1200']][reg['ID S-1200']] = reg
    arq.close()
        
    client = Client(URL_CONSULTA, transport=transport)
    client.set_options(cache=cache)
    for protocolo in registros:
        arquivo_consulta = core.DIR_CONSULTAS.joinpath(f'{protocolo}.json')
        if not arquivo_consulta.exists():
            result = client.service.ConsultarLoteEventos(consulta=Raw(consulta_lote_eventos(protocolo)))
            core.salvar_consulta(result)
        with open(arquivo_consulta) as arq:
            retorno_eventos = json.loads(arq.read())
        eventos = retorno_eventos['eSocial']['retornoProcessamentoLoteEventos']['retornoEventos']['evento']
        if isinstance(eventos, dict):
            eventos = [eventos]
        for evento in eventos:
            retorno_evento = evento['retornoEvento']['eSocial']['retornoEvento']
            id_ = retorno_evento['_Id']
            if id_ in registros[protocolo]:
                resposta = retorno_evento['processamento']['descResposta']
                if resposta == 'Sucesso.':
                    recibo = retorno_evento['recibo']['nrRecibo']
                    registros[protocolo][id_]['S-1200 Recibo'] = recibo
                    registros[protocolo][id_]['S-1200 Erro'] = ''
                else:
                    registros[protocolo][id_]['S-1200 Erro'] = resposta
    
    linhas = []
    for ids in registros.values():
        for reg in ids.values():
            linhas.append(reg)
    arq2 = open(arquivo, 'w', newline='\n')
    arq2_csv = csv.DictWriter(arq2, fieldnames=arq_csv.fieldnames, delimiter=';')
    arq2_csv.writeheader()
    arq2_csv.writerows(linhas)

def enviar_s1210():
    arq = open(arquivo)
    arq_csv = csv.DictReader(arq, delimiter=';')
    logger.info("Configurando eventos.")
    registros = defaultdict(dict)
    identificadores = {}
    lista_eventos = []
    for reg in arq_csv:
        registros[reg['CPF']] = reg
        if (reg['ID S-1210'] != '' and reg['S-1210 Erro'] == '') or reg['S-1200 Recibo'] == '':
            pprint(reg)
            continue
        dia, mes, ano = reg['Data do pagamento'].split('/')
        dt_pgto = XmlDate(
            year=int(ano),
            month=int(mes),
            day=int(dia),
        )
        per_ref = f'{ano}-{mes}'
        info_pg = montar_S1210_Pagamento(
            dt_pgto=dt_pgto,
            tp_pgto=S1210.InfoPgtoTpPgto.VALUE_1,
            per_ref=per_ref,
            dm_dev='001',
            valor=utils.txt_para_num(reg['Líquido'])
        )
        id_, evento = montar_S1210(
            cpf_benef='{0:>011}'.format(utils.limpar_doc(reg['CPF'])),
            per_ref=per_ref,
            pagamentos=[info_pg],
        )
        lista_eventos.append((id_, evento))
        registros[reg['CPF']]['ID S-1210'] = id_
        identificadores[id_] = reg['CPF']
    
    logger.info("Separando eventos em lotes.")
    lote_eventos = []
    while len(lista_eventos) > 50:
        lote_eventos.append(lista_eventos[:50])
        lista_eventos = lista_eventos[50:]
    lote_eventos.append(lista_eventos)

    client = Client(URL_ENVIO, transport=transport)
    client.set_options(cache=cache)
    logger.info("Enviando os lotes.")
    for lote in lote_eventos:
        lote_dct = dict(lote)
        lote_para_envio = envio_lote_eventos(evs=lote_dct, grupo=LoteEventosTipoGrupo.EVENTOS_PERIODICOS)
        result = client.service.EnviarLoteEventos(loteEventos=Raw(lote_para_envio))
        protocolo_envio = core.salvar_retorno(result) or ''
        logger.info("Lote enviado.")
        for evento in lote:
            cpf = identificadores[evento[0]]
            registros[cpf].update({
                'Protocolo de envio S-1210': protocolo_envio,
            })
    registros = list(registros.values())
    arq.close()
    if registros:
        arq2 = open(arquivo, 'w', newline='\n')
        arq2_csv = csv.DictWriter(arq2, fieldnames=list(registros[0].keys()), delimiter=';')
        arq2_csv.writeheader()
        arq2_csv.writerows(registros)

def consultar_s1210():
    arq = open(arquivo)
    arq_csv = csv.DictReader(arq, delimiter=';')
    registros = defaultdict(dict)
    for reg in arq_csv:
        if reg['Protocolo de envio S-1210'] and reg['ID S-1210']:
            registros[reg['Protocolo de envio S-1210']][reg['ID S-1210']] = reg
        else:
            registros[''][reg['CPF']] = reg
    arq.close()
        
    client = Client(URL_CONSULTA, transport=transport)
    client.set_options(cache=cache)
    for protocolo in registros:
        if protocolo == '':
            continue
        arquivo_consulta = core.DIR_CONSULTAS.joinpath(f'{protocolo}.json')
        if not arquivo_consulta.exists():
            result = client.service.ConsultarLoteEventos(consulta=Raw(consulta_lote_eventos(protocolo)))
            core.salvar_consulta(result)
        with open(arquivo_consulta) as arq:
            retorno_eventos = json.loads(arq.read())
        eventos = retorno_eventos['eSocial']['retornoProcessamentoLoteEventos']['retornoEventos']['evento']
        if isinstance(eventos, dict):
            eventos = [eventos]
        for evento in eventos:
            retorno_evento = evento['retornoEvento']['eSocial']['retornoEvento']
            id_ = retorno_evento['_Id']
            resposta = retorno_evento['processamento']['descResposta']
            if resposta == 'Sucesso.':
                recibo = retorno_evento['recibo']['nrRecibo']
                registros[protocolo][id_]['S-1210 Recibo'] = recibo
            else:
                registros[protocolo][id_]['S-1210 Erro'] = resposta
    
    linhas = []
    for ids in registros.values():
        for reg in ids.values():
            linhas.append(reg)
    arq2 = open(arquivo, 'w', newline='\n')
    arq2_csv = csv.DictWriter(arq2, fieldnames=arq_csv.fieldnames, delimiter=';')
    arq2_csv.writeheader()
    arq2_csv.writerows(linhas)