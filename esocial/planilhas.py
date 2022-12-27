from core import destino
from coletar import Planilha


class PlanilhaFolha(Planilha):
    conversor = {
        'Referência': 'per_apur',
        'ID S-1298': 'id_s1298',
        'Protocolo S-1298': 'protocolo_s1298',
        'Recibo S-1298': 'recibo_s1298',
        'Erro S-1298': 'erro_s1298',
        'ID S-1299': 'id_s1299',
        'Protocolo S-1299': 'protocolo_s1299',
        'Recibo S-1299': 'recibo_s1299',
        'Erro S-1299': 'erro_s1299',
    }
    estilos = {
        'centro': [
            'Referência',
            'ID S-1298', 'Protocolo S-1298', 'Recibo S-1298', 'Erro S-1298',
            'ID S-1299', 'Protocolo S-1299', 'Recibo S-1299', 'Erro S-1299',
        ]
    }
    identificador = 'per_apur'
    titulo = 'EventosFolha'

    def __init__(self) -> None:
        super().__init__(loc=destino.joinpath('Folhas.xlsx'))


class PlanilhaS3000(Planilha):
    conversor = {
        'Nº do recibo': 'nr_rec_evt',
        'Evento': 'tp_evento',
        'CPF do trabalhador': 'cpf_trab',
        'Ind. Per.': 'ind_apuracao',
        'Referência': 'per_apur',
        'Motivo': 'motivo',
        'ID S-3000': 'id_s3000',
        'Protocolo de envio S-3000': 'protocolo_s3000',
        'Recibo de envio S-3000': 'recibo_s3000',
        'Erro no envio S-3000': 'erro_s3000',
    }
    estilos = {
        'cpf': ['CPF do trabalhador'],
        'centro': [
            'Nº do recibo', 'Evento', 'Ind. Per.', 'Referência', 'ID S-3000',
            'Protocolo de envio S-3000', 'Recibo de envio S-3000',
        ]
    }
    identificador = 'nr_rec_evt'
    titulo = 'EventosS3000'

    def __init__(self) -> None:
        super().__init__(loc=destino.joinpath('Eventos S-3000.xlsx'))


class PlanilhaTotalizadorINSS(Planilha):
    conversor = {
        'Identificador': 'id_',
        'Competência': 'per_apur',
        'CPF': 'cpf',
        'Nome': 'nome',
        'Descontado': 'descontado',
        'Apurado': 'apurado',
        'Diferença': 'diferenca',
    }
    estilos = {
        'centro': ['Identificador', 'Competência'],
        'cpf': ['CPF'],
        'moeda': ['Descontado', 'Apurado', 'Diferença'],
    }
    identificador = 'id_'
    titulo = 'TotalizadorINSS'

    def __init__(self) -> None:
        super().__init__(loc=destino.joinpath(f'TotalizadorInss.xlsx'))