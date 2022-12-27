import locale
from argparse import ArgumentParser
from pathlib import WindowsPath

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

import loguru
import tomlkit
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

from bd import BancoDeDados
bd = BancoDeDados()


with WindowsPath(__file__).parent.joinpath('./perfis.toml').open() as f:
    cfg = tomlkit.parse(f.read())

perfis = cfg['perfis']

parser = ArgumentParser()
parser.add_argument(
    '-P', '--perfil',
    action='store',
    type=str,
    choices=perfis.keys(),
    required=True,
)
subparsers = parser.add_subparsers(help='sub-command help')

tipo_eventos = ['1200', '1210', '1298', '1299', '3000']

parser_esocial = subparsers.add_parser('esocial')
parser_esocial.add_argument('-p', '--producao', action='store_true')
parser_esocial.add_argument('-c', '--consulta', action='store_true')
parser_esocial.add_argument('-e', '--envio', action='store_true')
parser_esocial.add_argument(
    '-t', '--tipo',
    action='store',
    choices=tipo_eventos,
    type=str,
)

args = parser.parse_args()

if args.perfil:
    perfil = perfis[args.perfil]
    base = WindowsPath(perfil['base'])
    base.mkdir(exist_ok=True)
    destino = WindowsPath(perfil['destino'])
    origem = WindowsPath(perfil['origem'])
    bd.definir_loc(loc=base.joinpath(f'bd.{args.perfil}.json'))
    logger.add(base.joinpath('core.log'), level='DEBUG')
    logger.info(f"Processamento iniciado no perfil '{args.perfil}'.")
else:
    parser.print_help()