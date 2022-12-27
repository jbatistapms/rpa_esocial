from datetime import date, datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Final, Union

from xsdata.models.datatype import XmlDate


class LoteEventosTipoGrupo:
    EVENTOS_TABELA: Final = 1
    EVENTOS_NAO_PERIODICOS: Final = 2
    EVENTOS_PERIODICOS: Final = 3


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class TipoAmbiente(Enum):
    """
    Identificação do ambiente.

    :cvar VALUE_1: Produção
    :cvar VALUE_2: Produção restrita
    :cvar VALUE_7: Validação (uso interno)
    :cvar VALUE_8: Teste (uso interno)
    :cvar VALUE_9: Desenvolvimento (uso interno)
    """
    PRODUCAO = 1
    PRODUCAO_RESTRITA = 2
    VALIDACAO = 7
    TESTE = 8
    DESENVOLVIMENTO = 9


class TipoIncricao(Enum):
    CNPJ = 1
    CPF = 2


def obter_xmldate(data: Union[datetime, date, str, int]) -> tuple:
    if isinstance(data, (datetime, date)):
        return XmlDate.from_date(obj=data)
    if isinstance(data, int):
        data = datetime(1900, 1, 1) + timedelta(days=data-2)
        return XmlDate.from_date(obj=data)
    dia, mes, ano = data.split('/')
    return XmlDate(year=int(ano), month=int(mes), day=int(dia))

def limpar_data(data: str) -> str:
    return data.replace('/', '')

def limpar_doc(txt: str) -> str:
    if isinstance(txt, int):
        return txt
    return txt.replace('.', '').replace('-', '')

def txt_para_num(txt: str) -> str:
    if isinstance(txt, (int, float)):
        return Decimal(txt).quantize(Decimal("1.00"))
    return txt.replace('.', '').replace(',', '.')