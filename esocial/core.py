import json
import os
from datetime import datetime
from pathlib import WindowsPath
from typing import Any, Optional

from .utils import TipoAmbiente

TIPO_AMBIENTE: TipoAmbiente = None
VERSAO_LEIAUTE = 'S_1_0'

DIR_APLICATION = WindowsPath(os.getenv('DIR_APLICATION'))
DIR_APLICATION.mkdir(exist_ok=True)
DIR_CONSULTAS = DIR_APLICATION.joinpath('consultas')
DIR_CONSULTAS.mkdir(exist_ok=True)
DIR_ERROS = DIR_APLICATION.joinpath('erros')
DIR_ERROS.mkdir(exist_ok=True)
DIR_RETORNOS = DIR_APLICATION.joinpath('retornos')
DIR_RETORNOS.mkdir(exist_ok=True)

URL_WS = 'https://webservices.producaorestrita.esocial.gov.br/'
URL_WS_RESTRITO_BASE = URL_WS + 'servicos/empregador/'
URL_WS_ENV_RESTRITO = URL_WS_RESTRITO_BASE + 'enviarloteeventos/WsEnviarLoteEventos.svc'
URL_WS_REC_RESTRITO = URL_WS_RESTRITO_BASE + 'consultarloteeventos/WsConsultarLoteEventos.svc'

def ca_path() -> str:
    cert_path = WindowsPath(__file__).parent.joinpath('certificados')
    ca_path = cert_path.joinpath('ca.crt')
    if ca_path.exists():
        os.remove(ca_path)
    with ca_path.open('w') as arq:
        for origem in cert_path.iterdir():
            origem = cert_path.joinpath(origem)
            arq.write(origem.open().read())
    return str(ca_path)


def converter(dados) -> Any:
    if isinstance(dados, str):
        return dados
    elif isinstance(dados, list):
        rtrn = []
        for i in dados:
            rtrn.append(converter(i))
        return rtrn
    else:
        dct_rtrn = dict(dados)
        for k,v in dct_rtrn.items():
            dct_rtrn.update({k: converter(v)})
        return dct_rtrn

def salvar_consulta(retorno) -> None:
    dct_rtrn = converter(retorno)
    protocolo_envio = dct_rtrn['eSocial']['retornoProcessamentoLoteEventos']['dadosRecepcaoLote']['protocoloEnvio']
    with DIR_CONSULTAS.joinpath(f'{protocolo_envio}.json').open('w') as arq:
        arq.write(json.dumps(dct_rtrn, indent=4))

def salvar_retorno(retorno) -> Optional[str]:
    dct_rtrn = converter(retorno)
    estado_rtrn = dct_rtrn['eSocial']['retornoEnvioLoteEventos']
    if 'dadosRecepcaoLote' in estado_rtrn:
        protocolo_envio = estado_rtrn['dadosRecepcaoLote']['protocoloEnvio']
        with DIR_RETORNOS.joinpath(f'{protocolo_envio}.json').open('w') as arq:
            arq.write(json.dumps(dct_rtrn, indent=4))
        return protocolo_envio
    else:
        with DIR_ERROS.joinpath(f"{datetime.now().strftime('%Y.%m.%d.%H.%M.%S')}.json").open('w') as arq:
            arq.write(json.dumps(dct_rtrn, indent=4))
        return None

if __name__ == '__main__':
    print(ca_path())