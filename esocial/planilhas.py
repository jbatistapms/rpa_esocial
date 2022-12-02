from core import destino
from coletar import Planilha


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