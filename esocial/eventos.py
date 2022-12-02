import json
import secrets
import unicodedata
import xmlschema
from loguru import logger
from pathlib import WindowsPath

from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from lxml import etree
from suds.cache import FileCache
from suds.client import Client
from suds.sax.text import Raw
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.formats.dataclass.serializers.xml import XmlSerializer
from xsdata.models.datatype import XmlDate

from core import perfil

from . import core, token, utils
from .leiautes import *

from .leiautes.com.xsd.lote_eventos.consulta.consulta_lote_eventos_v1_0_0 import ESocial as ESocialConsultaLoteEventos
from .leiautes.com.xsd.lote_eventos.envio.envio_lote_eventos_v1_1_1 import *
from .transports import HttpTransportSuds

CNPJ8 = "29138393"
CNPJ11 = "29138393000186"

PROCESSO_EMISSAO: tipos.TsProcEmiSem8 = tipos.TsProcEmiSem8.VALUE_1
VERSAO_APLICATIVO = '0.1'

def url_consulta() -> str:
    final = '/servicos/empregador/consultarloteeventos/WsConsultarLoteEventos.svc?singleWsdl'
    if core.TIPO_AMBIENTE == utils.TipoAmbiente.PRODUCAO:
        return 'https://webservices.consulta.esocial.gov.br' + final
    return 'https://webservices.producaorestrita.esocial.gov.br' + final

def url_envio() -> str:
    final = '/servicos/empregador/enviarloteeventos/WsEnviarLoteEventos.svc?singleWsdl'
    if core.TIPO_AMBIENTE == utils.TipoAmbiente.PRODUCAO:
        return 'https://webservices.envio.esocial.gov.br' + final
    return 'https://webservices.producaorestrita.esocial.gov.br' + final

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
        xml_evento = XmlSerializer().render(obj=ev, ns_map=ns_map)
        xml_signer = token.assinar(xml=xml_evento)
        xml_string = etree.tostring(xml_signer)

        schema = xmlschema.XMLSchema(
            WindowsPath(__file__).parent.joinpath(ev.__class__.Meta.schema)
        )
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

def consulta_lote_eventos(protocolo_envio) -> str:
    esocial = ESocialConsultaLoteEventos(
        consulta_lote_eventos=ESocialConsultaLoteEventos.ConsultaLoteEventos(
            protocolo_envio=protocolo_envio
        )
    )
    xml_esocial = xml_serializer.render(
        obj=esocial,
        ns_map={None: "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00"}
    )
    with open('test_consulta_lote_eventos.xml', 'w') as arq:
        arq.write(xml_esocial)
    
    return xml_esocial

def montar_S1200(
        ind_retif: tipos.TsIndRetif, per_apur: str, cpf_trab: str, nome:str, dt_nasc: str, dm_dev_list: List,
        nr_recibo: Optional[str]=None, anual: bool=False,
        ) -> str:
    ide_evento = tipos.TIdeEventoFolha(
        ind_retif=ind_retif,
        nr_recibo=nr_recibo,
        ind_apuracao=tipos.TsIndApuracao.VALUE_2 if anual else tipos.TsIndApuracao.VALUE_1,
        per_apur=per_apur,
        tp_amb=core.TIPO_AMBIENTE,
        proc_emi=PROCESSO_EMISSAO,
        ver_proc=VERSAO_APLICATIVO,
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
        dm_dev=dm_dev_list,
        id=id_
    )
    return id_, S1200.Evento(evt_remun=evt_remun)

def montar_S1200_DmDev(
        identificador: str, cod_categ: str, cnpj_est: str, cbo: str, cod_lotacao: str,
        remuneracoes: List[S1200.TItensRemun], matricula: Optional[str]=None
        ):
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
    return S1200.Evento.EvtRemun.DmDev(
        ide_dm_dev=identificador,
        cod_categ=cod_categ,
        info_per_apur=info_per_apur,
        info_compl_cont=info_compl_cont,
    )

def montar_S1210(cpf_benef: str, per_ref: str, pagamentos=List[S1210.Evento.EvtPgtos.IdeBenef.InfoPgto]):
    ide_evento = tipos.TIdeEventoFolha(
        ind_retif=tipos.TsIndRetif.VALUE_1,
        per_apur=per_ref,
        tp_amb=core.TIPO_AMBIENTE,
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

def montar_S3000(
        tp_evento: str, nr_rec_evt: str, cpf_trab: str, 
        ind_apuracao: str, per_apur: str,
    ):
    ide_evento = tipos.TIdeEventoEvtTabInicial(
        tp_amb=core.TIPO_AMBIENTE,
        proc_emi=PROCESSO_EMISSAO,
        ver_proc=VERSAO_APLICATIVO,
    )
    ide_empregador = tipos.TIdeEmpregador(
        **IDE_EMPREGADOR
    )
    ide_trabalhador = S3000.Evento.EvtExclusao.InfoExclusao.IdeTrabalhador(
        cpf_trab=cpf_trab,
    )
    ide_folha_pagto = S3000.Evento.EvtExclusao.InfoExclusao.IdeFolhaPagto(
        ind_apuracao=ind_apuracao,
        per_apur=per_apur,
    )
    info_exclusao = S3000.Evento.EvtExclusao.InfoExclusao(
        tp_evento=tp_evento,
        nr_rec_evt=nr_rec_evt,
        ide_trabalhador=ide_trabalhador,
        ide_folha_pagto=ide_folha_pagto,
    )
    id_ = gerar_id()
    evt_exclusao = S3000.Evento.EvtExclusao(
        ide_evento=ide_evento,
        ide_empregador=ide_empregador,
        info_exclusao=info_exclusao,
        id=id_
    )
    return id_, S3000.Evento(evt_exclusao=evt_exclusao)

def enviar_s1200(registros):
    logger.info("Organizando dados de trabalho.")
    dados_ev = defaultdict(list)
    for rec in registros:
        if not rec['protocolo_s1200'] or rec['erro_s1200']:
            rec['id_s1200'] = ''
            rec['protocolo_s1200'] = ''
            rec['erro_s1200'] = ''
            dados_ev[rec['cpf']].append(rec)
    
    logger.info("Montando eventos.")
    eventos = []
    identificadores = defaultdict(list)
    for cpf, evt_list in dados_ev.items():
        valor = 0
        dsc_inss = 0
        dsc_irrf = 0
        dsc_iss = 0
        for evt in evt_list:
            valor += Decimal(utils.txt_para_num(evt['valor']))
            dsc_inss += Decimal(utils.txt_para_num(evt['dsc_inss']))
            dsc_irrf += Decimal(utils.txt_para_num(evt['dsc_irrf']))
            dsc_iss += Decimal(utils.txt_para_num(evt['dsc_iss']))
        
        remuneracao = S1200.TItensRemun(
            cod_rubr='REMUNERACAO',
            ide_tab_rubr='RPA',
            vr_rubr=valor,
            ind_apur_ir='0',
        )
        inss = S1200.TItensRemun(
            cod_rubr='INSS',
            ide_tab_rubr='RPA',
            vr_rubr=dsc_inss,
            ind_apur_ir='0',
        )
        irrf = S1200.TItensRemun(
            cod_rubr='IRRF',
            ide_tab_rubr='RPA',
            vr_rubr=dsc_irrf,
            ind_apur_ir='0',
        )
        iss = S1200.TItensRemun(
            cod_rubr='ISSQN',
            ide_tab_rubr='RPA',
            vr_rubr=dsc_iss,
            ind_apur_ir='0',
        )
        dia, mes, ano = dados_ev[cpf][0]['dt_nascimento'].split('/')
        dt_nasc = XmlDate(
            year=int(ano),
            month=int(mes),
            day=int(dia),
        )
        dia, mes, ano = dados_ev[cpf][0]['dt_final'].split('/')
        remuneracoes = [remuneracao, inss]
        if dsc_irrf > 0:
            remuneracoes.append(irrf)
        if dsc_iss > 0:
            remuneracoes.append(iss)

        demonstrativo = secrets.token_hex(12)
        s1200_dm_dv = montar_S1200_DmDev(
            identificador=demonstrativo,
            cod_categ=701,
            cnpj_est=perfil['cnpj'],
            cbo='{0:>06}'.format(utils.limpar_doc(dados_ev[cpf][0]['cbo'])),
            cod_lotacao='001',
            remuneracoes=remuneracoes
        )
        nome = unicodedata.normalize(
            "NFKD", dados_ev[cpf][0]['nome']
        ).encode(
            'ASCII', 'ignore'
        ).decode().upper().strip()
        id_, evento = montar_S1200(
            ind_retif=tipos.TsIndRetif.VALUE_1,
            per_apur=f'{ano}-{mes}',
            cpf_trab='{0:>011}'.format(utils.limpar_doc(cpf)),
            nome=nome,
            dt_nasc=dt_nasc,
            dm_dev_list=[s1200_dm_dv],
        )
        eventos.append((id_, evento))
        for evt in evt_list:
            identificadores[id_].append(evt)
            evt['nome'] = nome
            evt['id_s1200'] = id_
            evt['demonstrativo'] = demonstrativo

    logger.info("Separando eventos em lotes.")
    lote_eventos = []
    while len(eventos) > 50:
        lote_eventos.append(eventos[:50])
        eventos = eventos[50:]
    lote_eventos.append(eventos)

    client = Client(url_envio(), transport=transport)
    client.set_options(cache=cache)
    logger.info("Enviando os lotes.")
    for lote in lote_eventos:
        lote_dct = dict(lote)
        lote_para_envio = envio_lote_eventos(evs=lote_dct, grupo=utils.LoteEventosTipoGrupo.EVENTOS_PERIODICOS)
        result = client.service.EnviarLoteEventos(loteEventos=Raw(lote_para_envio))
        protocolo_envio = core.salvar_retorno(result) or ''
        logger.info("Lote enviado.")
        for id_evento in lote_dct.keys():
            for evt in identificadores[id_evento]:
                evt['protocolo_s1200'] = protocolo_envio

def consultar_s1200(registros):
    logger.info("Organizando dados para processamento.")
    dados_evt = defaultdict(list)
    dados_reg = defaultdict(list)
    for reg in registros:
        dados_evt[reg['protocolo_s1200']].append(reg['id_s1200'])
        dados_reg[reg['id_s1200']].append(reg)

    client = Client(url_consulta(), transport=transport)
    client.set_options(cache=cache)
    for protocolo in dados_evt:
        logger.info(f"Obtendo dados do protocolo {protocolo}.")
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
            if id_ in dados_evt[protocolo]:
                resposta = retorno_evento['processamento']['descResposta']
                if resposta == 'Sucesso.':
                    recibo = retorno_evento['recibo']['nrRecibo']
                    for reg in dados_reg[id_]:
                        reg['recibo_s1200'] = recibo
                        reg['erro_s1200'] = ''
                else:
                    dscr_resp = [resposta]
                    ocorrencias = retorno_evento['processamento']['ocorrencias']
                    if not isinstance(ocorrencias, list):
                        ocorrencias = [ocorrencias]
                    for ocorr in ocorrencias:
                        dscr_resp.append(ocorr['ocorrencia']['descricao'])
                    for reg in dados_reg[id_]:
                        reg['erro_s1200'] = '\n'.join(dscr_resp)

def enviar_s1210(registros):
    logger.info("Preparando dados.")
    dados_evt = defaultdict(list)
    for reg in registros:
        if not reg['recibo_s1210'] and reg['recibo_s1200'] and reg['dt_pgto'] and (not reg['id_s1210'] or reg['S-1210 Erro']):
            dados_evt[reg['cpf']].append(reg)
    
    lista_eventos = []
    identificador = defaultdict(list)
    for cpf, evts in dados_evt.items():
        dm_val = Decimal('0')
        for ev in evts:
            dm_val += Decimal(utils.txt_para_num(ev['v_liquido']))
        
        dados = evts[0]
        dt_pgto = XmlDate.from_datetime(dados['dt_pgto'])
        per_ref = dados['dt_pgto'].strftime("%Y-%m")
        info_pg = montar_S1210_Pagamento(
            dt_pgto=dt_pgto,
            tp_pgto=S1210.InfoPgtoTpPgto.VALUE_1,
            per_ref=per_ref,
            dm_dev=dados['demonstrativo'],
            valor=dm_val,
        )
        id_, evento = montar_S1210(
            cpf_benef='{0:>011}'.format(dados['cpf']),
            per_ref=per_ref,
            pagamentos=[info_pg],
        )
        lista_eventos.append((id_, evento))
        identificador[id_] = cpf
        for ev in evts:
            ev['id_s1210'] = id_
    
    logger.info("Separando eventos em lotes.")
    lote_eventos = []
    while len(lista_eventos) > 50:
        lote_eventos.append(lista_eventos[:50])
        lista_eventos = lista_eventos[50:]
    lote_eventos.append(lista_eventos)

    client = Client(url_envio(), transport=transport)
    client.set_options(cache=cache)
    logger.info("Enviando os lotes.")
    for lote in lote_eventos:
        lote_dct = dict(lote)
        lote_para_envio = envio_lote_eventos(
            evs=lote_dct,
            grupo=utils.LoteEventosTipoGrupo.EVENTOS_PERIODICOS,
        )
        result = client.service.EnviarLoteEventos(loteEventos=Raw(lote_para_envio))
        protocolo_envio = core.salvar_retorno(result) or ''
        logger.info("Lote enviado.")
        for evento in lote:
            cpf = identificador[evento[0]]
            for evt in dados_evt[cpf]:
                evt['protocolo_s1210'] = protocolo_envio

def consultar_s1210(registros):
    dados = defaultdict(list)
    lista_registros = defaultdict(list)
    for reg in registros:
        if reg['protocolo_s1210'] and reg['id_s1210']:
            dados[reg['protocolo_s1210']].append(reg['id_s1210'])
            lista_registros[reg['id_s1210']].append(reg)
        
    client = Client(url_consulta(), transport=transport)
    client.set_options(cache=cache)
    for protocolo in dados:
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
                for reg in lista_registros[id_]:
                    reg['recibo_s1210'] = recibo
            else:
                dscr_resp = [resposta]
                ocorrencias = retorno_evento['processamento']['ocorrencias']
                if not isinstance(ocorrencias, list):
                    ocorrencias = [ocorrencias]
                for ocorr in ocorrencias:
                    dscr_resp.append(ocorr['ocorrencia']['descricao'])
                for reg in lista_registros[id_]:
                    reg['erro_s1210'] = '\n'.join(dscr_resp)

def enviar_s3000(registros) -> None:
    logger.info("Preparando e criando eventos S-3000.")
    list_reg = {}
    lista_eventos = []
    for reg in registros:
        if reg['recibo_s3000'] or (reg['protocolo_s3000'] and not reg['erro_s3000']):
            continue
        id_, evento = montar_S3000(
            per_apur=reg['per_apur'],
            tp_evento=reg['tp_evento'],
            nr_rec_evt=reg['nr_rec_evt'],
            cpf_trab=reg['cpf_trab'],
            ind_apuracao=reg['ind_apuracao'],
        )
        reg['id_s3000'] = id_
        lista_eventos.append((id_, evento))
        list_reg[id_] = reg
    
    logger.info("Separando eventos em lotes.")
    lote_eventos = []
    while len(lista_eventos) > 50:
        lote_eventos.append(lista_eventos[:50])
        lista_eventos = lista_eventos[50:]
    lote_eventos.append(lista_eventos)

    client = Client(url_envio(), transport=transport)
    client.set_options(cache=cache)
    logger.info("Enviando os lotes.")
    for lote in lote_eventos:
        lote_dct = dict(lote)
        lote_para_envio = envio_lote_eventos(
            evs=lote_dct,
            grupo=utils.LoteEventosTipoGrupo.EVENTOS_NAO_PERIODICOS,
        )
        result = client.service.EnviarLoteEventos(loteEventos=Raw(lote_para_envio))
        protocolo_envio = core.salvar_retorno(result) or ''
        logger.info("Lote enviado.")
        for id_ in lote_dct.keys():
            list_reg[id_]['protocolo_s3000'] = protocolo_envio

def consultar_s3000(registros):
    dados = defaultdict(list)
    lista_registros = {}
    for reg in registros:
        if reg['protocolo_s3000'] and reg['id_s3000']:
            dados[reg['protocolo_s3000']].append(reg['id_s3000'])
            lista_registros[reg['id_s3000']] = reg
        
    client = Client(url_consulta(), transport=transport)
    client.set_options(cache=cache)
    for protocolo in dados:
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
                lista_registros[id_]['recibo_s3000'] = recibo
            else:
                dscr_resp = [resposta]
                ocorrencias = retorno_evento['processamento']['ocorrencias']
                if not isinstance(ocorrencias, list):
                    ocorrencias = [ocorrencias]
                for ocorr in ocorrencias:
                    dscr_resp.append(ocorr['ocorrencia']['descricao'])
                lista_registros[id_]['erro_s3000'] = '\n'.join(dscr_resp)