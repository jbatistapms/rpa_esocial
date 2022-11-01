import csv, decimal, os, sys, unicodedata, uuid
from lib2to3.pgen2.token import OP
from argparse import ArgumentParser
from collections import OrderedDict
from hashlib import md5
from openpyxl import Workbook
from openpyxl.styles import Alignment, NamedStyle
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from pathlib import Path, WindowsPath
from typing import Dict, List, Optional, Tuple

from dotenv import load_dotenv
from loguru import logger
from tinydb import where, TinyDB
load_dotenv()

DIR_DEV = WindowsPath.cwd().joinpath('dev')
DIR_DEV.mkdir(exist_ok=True)
COMPETENCIA = os.getenv('COMPETENCIA', None)

bd = TinyDB(DIR_DEV.joinpath('bd.json'))

TblArquivos = bd.table('arquivos')
TblPessoas = bd.table('pessoas')
TblRecibos = bd.table('recibos')

ctx_decimal = decimal.getcontext()
ctx_decimal.rounding = decimal.ROUND_HALF_EVEN

class Arquivo(object):
    def __init__(self, loc: WindowsPath) -> None:
        self.__loc = loc
        self.__logs_pln = []
        self.__recibos: List[Recibo] = []
        with loc.open() as arq:
            for ln in arq.readlines():
                if ln.startswith("tipo»R"):
                    self.__recibos.append(Recibo.importar_texto(text=ln))
    
    def __repr__(self) -> str:
        return repr(self.__loc)
    
    def __str__(self) -> str:
        return str(self.__loc)
    
    def extensao(self) -> str:
        return self.__loc.suffix
    
    def logs_planilha(self) -> List:
        return self.__logs_pln
    
    def nome(self) -> str:
        return self.__loc.stem
    
    def recibos(self) -> List['Recibo']:
        return self.__recibos
    
    def salvar(self) -> None:
        for rec in self.__recibos:
            rec.salvar()
        TblArquivos.insert({'id': self.nome()})


class Coletor(object):
    def __init__(self, origem: WindowsPath) -> None:
        self.__origem: WindowsPath = origem
        self.__origem.mkdir(exist_ok=True)
    
    def __validar_arquivo(self, arq: WindowsPath) -> bool:
        try:
            uuid.UUID(arq.stem)
        except:
            logger.error(f"Nome de arquivo '{arq.stem}' não é válido.")
        else:
            if TblArquivos.get(where('id')==arq.stem) is None:
                return arq.suffix == '.txt'
        return False
    
    def arquivos(self) -> List[Arquivo]:
        self.__arquivos = [
            Arquivo(loc=arq) for arq in self.__origem.iterdir()
            if self.__validar_arquivo(arq=arq)
        ]
        return self.__arquivos
    
    def salvar(self) -> None:
        for arq in self.arquivos():
            arq.salvar()


class Controlador(object):
    def __init__(self, destino: WindowsPath) -> None:
        self.__destino: WindowsPath = destino
        self.__destino.mkdir(exist_ok=True)
        if COMPETENCIA:
            mes, ano = COMPETENCIA.split('/')
            self.__loc_recibos = self.__destino.joinpath(f'{ano}.{mes}.xlsx')
        else:
            self.__loc_recibos = self.__destino.joinpath('recibos.xlsx')
    
    def __exportar_recibos(self, recibos: List[dict], dst: WindowsPath) -> None:
        if len(recibos) > 0:
            cabecalho = list(recibos[0].keys())
            alinhamento_centro = Alignment(horizontal='center')
            tipo_cbo = NamedStyle(
                name='cbo',
                number_format='0000"-"00',
                alignment=alinhamento_centro,
            )
            tipo_cpf = NamedStyle(
                name='cpf',
                number_format='000"."000"."000"-"00',
                alignment=alinhamento_centro,
            )
            tipo_data = NamedStyle(
                name='data',
                number_format='dd/mm/yyyy',
                alignment=alinhamento_centro,
            )
            tipo_moeda = NamedStyle(
                name='moeda',
                number_format='#,##0.00',
            )
            tipo_nit = NamedStyle(
                name='nit',
                number_format='000"."00000"."00"-"0',
                alignment=alinhamento_centro,
            )
            criar_planilha(
                cbc=cabecalho,
                lns=[list(i.values()) for i in recibos],
                loc=dst,
                estilo={
                    tipo_data: ['Data inicial', 'Data de nascimento', 'Data final'],
                    tipo_cpf: ['CPF'],
                    tipo_nit: ['NIS/PIS'],
                    tipo_cbo: ['CBO'],
                    tipo_moeda: [
                        'Valor', 'Dsc. INSS', 'Dif. INSS', 'Dsc. IRRF', 'Dsc. ISS', 
                        'Valor - Outros descontos I', 'Valor - Outros descontos II',
                        'Líquido'
                    ],
                }
            )
    
    def __extrair_dados(self, linha) -> dict:
        rec_temp = OrderedDict()
        rec_temp['Nome'] = linha['nome']
        rec_temp['CPF'] = linha['cpf']
        rec_temp['Data de nascimento'] = linha['dt_nascimento']
        rec_temp['NIS/PIS'] = linha['nis_pis']
        rec_temp['CBO'] = linha['cbo']
        rec_temp['Serviço prestado'] = linha['servico_prestado']
        rec_temp['Data inicial'] = linha['dt_inicial']
        rec_temp['Data final'] = linha['dt_final']
        rec_temp['Valor'] = linha['valor']
        rec_temp['Dsc. INSS'] = linha['dsc_inss']
        rec_temp['Dif. INSS'] = linha.get('dif_inss', '')
        rec_temp['Dsc. IRRF'] = linha['dsc_irrf']
        rec_temp['Dsc. ISS'] = linha['dsc_iss']
        rec_temp['Descrição - Outros descontos I'] = linha['outrosd_desc1']
        rec_temp['Valor - Outros descontos I'] = linha['outrosd_valor1']
        rec_temp['Descrição - Outros descontos II'] = linha['outrosd_desc2']
        rec_temp['Valor - Outros descontos II'] = linha['outrosd_valor2']
        rec_temp['Líquido'] = linha['v_liquido']
        rec_temp['Órgão contratante'] = linha['orgao']
        rec_temp['Erros'] = linha['erros']
        return rec_temp

    def exportar_qcadastral(self) -> None:
        logger.debug("Iniciando exportação de dados de pessoal para qualificação cadastral")
        pessoas = []
        for ps in TblPessoas.search((where('qcadastral')=='NÃO') | (where('qcadastral')=='ERRO')):
            ps_qc = OrderedDict()
            ps_qc['CPF'] = f"{ps['cpf']:>011}"
            ps_qc['NIS'] = f"{ps['nis_pis']:>011}"
            ps_qc['NOME'] = ps['nome']
            ps_qc['DN'] = limpar_doc(ps['dt_nascimento'])
            pessoas.append(ps_qc)
        salvar_dados(dados=pessoas, dst=self.__destino.joinpath('qualificacao_cadastral.txt'))
    
    def exportar_recibos(self) -> None:
        recibos = []
        if self.__loc_recibos.exists():
            with self.__loc_recibos.open() as arq_rec:
                recibos += [] # list(csv.DictReader(arq_rec, delimiter=';'))
        if COMPETENCIA:
            condicao_bd = (
                (where('dt_final').search(f'{COMPETENCIA}')) &
                (where('exportado') == False)
            )
            recibos_bd = TblRecibos.search(condicao_bd)
        else:
            condicao_bd = None
            if self.__loc_recibos.exists():
                os.remove(self.__loc_recibos)
            recibos_bd = TblRecibos.all()
        recibos += [self.__extrair_dados(i) for i in recibos_bd]
        self.__exportar_recibos(
            recibos=recibos,
            dst=self.__loc_recibos,
        )
        if condicao_bd:
            TblRecibos.update({'exportado': True}, cond=condicao_bd)
        
class Recibo(object):
    def __init__(self, **dados) -> None:
        self.__erros = []
        self.__dados = dados
        self.__dados.update({'qcadastral': 'NÃO', 'erros': '', 'exportado': False})
        self.__tratar_dados()
        self.__dados_pessoa = copiar_dict(
            obj=self.__dados,
            inc=['cpf', 'dt_nascimento', 'nis_pis', 'nome', 'qcadastral']
        )

    def __tratar_dados(self) -> dict:
        self.__erros = []
        self.__dados.update({
            'nome': unicodedata.normalize(
                "NFKD", self.__dados['nome']
                ).encode(
                    'ASCII', 'ignore'
                ).decode(),
        })
        # Campos com valores
        for cmp in [
                'dsc_inss', 'dsc_irrf', 'dsc_iss', 'valor', 'v_liquido', 
                'outrosd_valor1', 'outrosd_valor2'
            ]:
            if self.__dados[cmp] == '':
                self.__dados[cmp] = 0
            valor, erro = normalizar_valor(text=self.__dados[cmp])
            if erro:
                self.__erros.append(erro)
            else:
                self.__dados[cmp] = valor
        # Campo com datas
        for cmp in ['dt_final', 'dt_inicial', 'dt_nascimento']:
            valor, erro = normalizar_data(text=self.__dados[cmp])
            if erro:
                self.__erros.append(erro)
            else:
                self.__dados.update({cmp: valor})
        # PIS
        nis_pis_org = self.__dados['nis_pis']
        nis_pis = limpar_doc(nis_pis_org)
        if len(nis_pis) != 11 and nis_pis.isdigit():
            self.__erros.append(f'Número de NIS deve possuir 11 dígitos: {nis_pis_org}')
        else:
            nis_pis = int(nis_pis)
        # CPF
        cpf_org = self.__dados['cpf']
        cpf = limpar_doc(cpf_org)
        if len(cpf) != 11 or not cpf.isdigit():
            self.__erros.append(f'Número de CPF deve possuir 11 dígitos: {cpf_org}')
        else:
            cpf = int(cpf)
        # CBO
        cbo_org = self.__dados['cbo']
        cbo = limpar_doc(cbo_org)
        if len(cbo) != 6 or not cbo.isdigit():
            self.__erros.append(f'CBO deve possuir 6 dígitos: {cbo_org}')
        else:
            cbo = int(cbo)
        # Atualizar
        self.__dados.update({'nis_pis': nis_pis})
        self.__dados.update({'cpf': cpf})
        self.__dados.update({'cbo': cbo})
        for erro in self.__erros:
            self.__dados['erros'] += erro + ';'
        # Diferença INSS
        valor = decimal.Decimal(self.__dados[cmp]['valor'])
        inss = valor * decimal.Decimal('0.11')
        inss = inss.quantize(decimal.Decimal('1.00'))
        dif = decimal.Decimal(self.__dados[cmp]['dsc_inss']) - inss
        self.__dados.update({'dif_inss': f'R$ {dif}'.replace('.', ',')})
        # Valor líquido
        v_liquido = decimal.Decimal(self.__dados[cmp]['valor'])
        for cmp in ['dsc_inss', 'dsc_irrf', 'dsc_iss', 'outrosd_valor1', 'outrosd_valor2']:
            v_liquido -= decimal.Decimal(self.__dados[cmp][cmp])
        self.__dados.update({'v_liquido': f'R$ {v_liquido}'.replace('.', ',')})
    
    def erros(self) -> str:
        erros = ''
        for erro in self.__erros:
            erros += erro + ';'
        return erros if len(erros) > 0 else None
    
    @classmethod
    def importar_texto(cls, text: str) -> 'Recibo':
        dados = {}
        for ch_vl in text.split('«')[:-1]:
            ch, vl = ch_vl.split('»')
            dados.update({ch: vl})
        dados.update({'id': str(uuid.UUID(md5(text.encode()).hexdigest()))})
        return cls(**dados)
    
    def salvar(self) -> None:
        pessoa_db = TblPessoas.get(where('cpf')==self.__dados['cpf'])
        if pessoa_db is None and self.__dados['erros'] == '':
            TblPessoas.insert(self.__dados_pessoa)
        recibo_db = TblRecibos.get(where('id')==self.__dados['id'])
        if recibo_db is None:
            TblRecibos.insert(self.__dados)


def copiar_dict(obj: dict, exc: Optional[List[str]]=None, inc: Optional[List[str]]=None) -> dict:
    rtrn = {}
    if inc:
        for opc in inc:
            if opc in obj:
                rtrn.update({opc: obj[opc]})
    elif exc:
        rtrn = obj.copy()
        for opc in exc:
            if opc in obj:
                rtrn.pop(opc)
    else:
        rtrn = obj.copy()
    return rtrn

def limpar_doc(doc_txt: str) -> str:
    return doc_txt.replace('.', '').replace('-', '').replace('/', '')

def normalizar_data(text: str) -> str:
    data = text.replace('/', '')
    if len(data) != 8:
        return None, f"Data ilegível: {text}"
    return f"{data[0:2]}/{data[2:4]}/{data[4:8]}", None

def normalizar_valor(text: str) -> Tuple[Optional[float],Optional[str]]:
    if text in ['', '0', 0]:
        return 0, None
    elif text.startswith('R$ '):
        try:
            _, valor = text.split()
            return float(valor.replace('.', '').replace(',', '.')), None
        except Exception as erro:
            return None, f"Valor '{text}' não corresponde ao esperado: {erro}"
    else:
        return None, f"Valor '{text}' não corresponde ao esperado."

def salvar_dados(dados: List[dict], dst: Path, fieldnames: Optional[List]=None) -> None:
    with dst.open('w', newline='') as arq:
        if dados:
            fieldnames = fieldnames or list(dados[0].keys())
            arq_csv = csv.DictWriter(arq, fieldnames=fieldnames, delimiter=';')
            arq_csv.writeheader()
            arq_csv.writerows(dados)
        else:
            arq.write('')

def criar_planilha(cbc: List, lns: List[List], loc: WindowsPath, estilo: Optional[Dict]):
    wb = Workbook()
    ws = wb.active

    # Escrever cabeçalho
    ws.append(cbc)
    
    # Escrever linhas
    for lista in lns:
        ws.append(lista)
    
    colunas = list(ws.columns)
    
    # Criar tabela e definir estilo
    style = TableStyleInfo(
        name="TableStyleLight15",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    column = list(ws.columns)[-1][0].column_letter
    tab = Table(
        displayName="Recibos",
        ref=f"A1:{column}{len(lns)+1}",
        tableStyleInfo=style,
    )
    ws.add_table(tab)

    # Centralizar cabeçalho
    for row in ws.iter_rows(min_row=1, max_col=len(cbc), max_row=1):
        for cell in row:
            cell.alignment = Alignment(horizontal='center')

    # Redimensionamento
    for col_n, column_cells in enumerate(colunas):
        new_column_length = max(
            [len(str(cell.value)) for cell in column_cells] +
            [len(cbc[col_n])+5]
        )
        new_column_letter = get_column_letter(column_cells[0].column)
        if new_column_length > 0:
            ws.column_dimensions[new_column_letter].width = new_column_length*1.25
    
    # Aplicar estilos
    if isinstance(estilo, dict):
        for stl, colunas in estilo.items():
            wb.add_named_style(stl)
            for col_nome in colunas:
                idx = cbc.index(col_nome) + 1
                for col in ws.iter_cols(min_col=idx, max_col=idx, min_row=2, max_row=len(lns)*2):
                    for cell in col:
                        cell.style = stl.name

    # Salvar arquivo
    wb.save(loc)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--producao', action='store_true', default=False)
    parser.add_argument('-t', '--teste', action='store_true', default=False)
    args = parser.parse_args()
    if args.teste:
        origem = DIR_DEV.joinpath('origem')
        destino = DIR_DEV.joinpath('destino')
    elif args.producao:
        destino = WindowsPath(os.getenv('DROPBOX_DIR'))
        origem = destino.joinpath('rpa')
        bd = TinyDB(destino.joinpath('bd.json'))
        TblArquivos = bd.table('arquivos')
        TblPessoas = bd.table('pessoas')
        TblRecibos = bd.table('recibos')
    else:
        parser.print_help()
        sys.exit()
    
    logger.add(DIR_DEV.joinpath('coletor.log'), level='INFO')

    colt = Coletor(origem=origem)
    colt.salvar()
    exp = Controlador(destino=destino)
    exp.exportar_qcadastral()
    exp.exportar_recibos()