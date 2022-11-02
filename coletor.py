import csv, decimal, os, sys, unicodedata, uuid
from lib2to3.pgen2.token import OP
from argparse import ArgumentParser
from collections import defaultdict, OrderedDict
from hashlib import md5
from openpyxl import load_workbook, Workbook
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

titulo_excel_recibo = {
    'Nome': 'nome',
    'CPF': 'cpf',
    'Data de nascimento': 'dt_nascimento',
    'NIS/PIS': 'nis_pis',
    'CBO': 'cbo',
    'Serviço prestado': 'servico_prestado',
    'Data inicial': 'dt_inicial',
    'Data final': 'dt_final',
    'Valor': 'valor',
    'Dsc. INSS': 'dsc_inss',
    'Dif. INSS': 'dif_inss',
    'Dsc. IRRF': 'dsc_irrf',
    'Dsc. ISS': 'dsc_iss',
    'Descrição - Outros descontos I': 'outrosd_desc1',
    'Valor - Outros descontos I': 'outrosd_valor1',
    'Descrição - Outros descontos II': 'outrosd_desc2',
    'Valor - Outros descontos II': 'outrosd_valor2',
    'Líquido': 'v_liquido',
    'Órgão contratante': 'orgao',
    'Erros': 'erros',
}
titulo_recibo_excel = {v: k for k, v in titulo_excel_recibo.items()}


class Arquivo(object):
    def __init__(self, loc: WindowsPath) -> None:
        self.__loc = loc
        self.__logs_pln = []
        self.__recibos: List[Recibo] = []
        with loc.open() as arq:
            for ln in arq.readlines():
                if ln.startswith("tipo»R"):
                    self.__recibos.append(Recibo.novo_de_texto(text=ln))
    
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
    
    def __exportar_recibos(self, recibos: List['Recibo'], dst: WindowsPath) -> None:
        if len(recibos) > 0:
            cabecalho = list(titulo_excel_recibo.keys())
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
                lns=[list(rec.dados_planilha()) for rec in recibos],
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

    def exportar_qcadastral(self) -> None:
        logger.debug("Iniciando exportação de dados de pessoal para qualificação cadastral")
        pessoas = []
        with self.__destino.joinpath('qualificacao_cadastral.txt').open('w') as arq:
            for ps in TblPessoas.search((where('qcadastral')=='NÃO') | (where('qcadastral')=='ERRO')):
                arq.write(f"{ps['cpf']:>011};{ps['nis_pis']:>011};{ps['nome']};{limpar_doc(ps['dt_nascimento'])}\n")
    
    def exportar_recibos(self) -> None:
        recibos = []
        if self.__loc_recibos.exists():
            recibos += ler_planilha(loc=self.__loc_recibos)
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
        recibos += [Recibo(**dados) for dados in recibos_bd]
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
        self.__tratar_dados()
        self.__dados_pessoa = copiar_dict(
            obj=self.__dados,
            inc=['cpf', 'dt_nascimento', 'nis_pis', 'nome', 'qcadastral']
        )
    
    def __limpar_doc(self, cmp: str, cont: int) -> None:
        valor = self.__dados[cmp]
        cmp_exc = titulo_recibo_excel[cmp]
        if isinstance(valor, str):
            vl_retorno = self.__dados[cmp]
            for caracter in '.-/_':
                vl_retorno = vl_retorno.replace(caracter, '')
            if vl_retorno.isdigit() and len(vl_retorno) == cont:
                valor = int(vl_retorno)
            else:
                self.__erros.append(f"Número de '{cmp_exc}' deve possuir {cont} dígitos: {valor}")
        elif isinstance(valor, int):
            if not valor < 10**cont:
                self.__erros.append(f"Número de '{cmp_exc}' deve possuir {cont} dígitos: {valor}")
        else:
            self.__erros.append(f"Número de '{cmp_exc}' não reconhecido: {valor}")
        self.__dados[cmp] = valor

    def __tratar_dados(self) -> dict:
        self.__dados['erros'] = ''
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
            valor, erro = normalizar_valor(valor=self.__dados[cmp])
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
        # Noemalizar documentos
        self.__limpar_doc(cmp='nis_pis', cont=11)
        self.__limpar_doc(cmp='cpf', cont=11)
        self.__limpar_doc(cmp='cbo', cont=6)
        for erro in self.__erros:
            self.__dados['erros'] += erro + ';'
        # Diferença INSS
        valor = decimal.Decimal(self.__dados['valor'])
        inss = valor * decimal.Decimal('0.11')
        inss = float(inss.quantize(decimal.Decimal('1.00')))
        self.__dados.update({'dif_inss': self.__dados['dsc_inss'] - inss})
        # Valor líquido
        v_liquido = self.__dados['valor']
        for cmp in ['dsc_inss', 'dsc_irrf', 'dsc_iss', 'outrosd_valor1', 'outrosd_valor2']:
            v_liquido -= self.__dados[cmp]
        self.__dados.update({'v_liquido': v_liquido})
        # Outros descontos
        if self.__dados['outrosd_desc1'] == '0':
            self.__dados['outrosd_desc1'] = ''
        if self.__dados['outrosd_desc2'] == '0':
            self.__dados['outrosd_desc2'] = ''
    
    def dados_planilha(self) -> dict:
        rec_temp = OrderedDict()
        for exc, txt in titulo_excel_recibo.items():
            rec_temp[exc] = self.__dados.get(txt, '')
        return rec_temp.values()
    
    def erros(self) -> str:
        erros = ''
        for erro in self.__erros:
            erros += erro + ';'
        return erros if len(erros) > 0 else None
    
    @classmethod
    def novo_de_texto(cls, text: str) -> 'Recibo':
        dados = {'qcadastral': 'NÃO', 'erros': '', 'exportado': False}
        for ch_vl in text.split('«')[:-1]:
            ch, vl = ch_vl.split('»')
            dados.update({ch: vl})
        return cls(**dados)
    
    def salvar(self) -> None:
        pessoa_db = TblPessoas.get(where('cpf')==self.__dados['cpf'])
        if pessoa_db is None and self.__dados['erros'] == '':
            TblPessoas.insert(self.__dados_pessoa)
        assinatura_recibo = (str(self.__dados['cbo']) +
            str(self.__dados['cpf']) +
            str(self.__dados['dt_final']) +
            str(self.__dados['orgao']) +
            str(self.__dados['valor'])
        )
        self.__dados['id'] = str(uuid.UUID(md5(assinatura_recibo.encode()).hexdigest()))
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

def normalizar_valor(valor: str) -> Tuple[Optional[float],Optional[str]]:
    if valor in ['', '0', 0]:
        return 0, None
    elif isinstance(valor, (int, float)):
        return valor, None
    elif valor.startswith('R$ '):
        try:
            _, valor = valor.split()
            return float(valor.replace('.', '').replace(',', '.')), None
        except Exception as erro:
            return None, f"Valor '{valor}' não corresponde ao esperado: {erro}"
    else:
        return None, f"Valor '{valor}' não corresponde ao esperado."

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
    ws.title = 'Recibos'

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
        displayName="recibos",
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

def ler_planilha(loc: WindowsPath) -> List[Recibo]:
    wb = load_workbook(loc)
    ws = wb['Recibos']
    lista_linhas = []
    for row in ws.rows:
        linha = []
        for cell in row:
            linha.append(cell.value)
        lista_linhas.append(linha)
    cabecalho = lista_linhas.pop(0)
    recibos = []
    for linha in lista_linhas:
        dados = defaultdict()
        for exc, txt in titulo_excel_recibo.items():
            try:
                idx = cabecalho.index(exc)
            except:
                logger.error(f"Coluna {exc} inexistente em {loc}")
                sys.exit()
            dados[txt] = linha[idx]
        if dados['nome'] is not None:
            recibos.append(Recibo(**dados))
    return recibos

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