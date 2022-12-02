import sys

from loguru import logger

from coletar import Controlador, destino
from core import args
from esocial import core as core_esocial
from esocial.eventos import consultar_s1200, consultar_s1210, enviar_s1200, enviar_s1210
from esocial.utils import TipoAmbiente


tipo_eventos = ['1200', '1210']

if __name__ == '__main__':
    if args.producao:
        if input("Iniciar em modo de produção? (S para sim, qualquer valor para não): ") != "S":
            sys.exit()
        core_esocial.TIPO_AMBIENTE = TipoAmbiente.PRODUCAO
        logger.warning("Iniciando interação com o webservice do eSocial no ambiente de PRODUÇÃO.")
    else:
        core_esocial.TIPO_AMBIENTE = TipoAmbiente.PRODUCAO_RESTRITA
        logger.info("Iniciando interação com o webservice do eSocial no ambiente de PRODUÇÃO RESTRITA.")
    
    ctrl = Controlador(destino=destino)
    if args.envio:
        if args.tipo == '1200':
            enviar_s1200(registros=ctrl.pln_recibos.registros())
            ctrl.pln_recibos.gravar()
        elif args.tipo == '1210':
            enviar_s1210(registros=ctrl.pln_recibos.registros())
            ctrl.pln_recibos.gravar()
    elif args.consulta:
        if args.tipo == '1200':
            consultar_s1200(registros=ctrl.pln_recibos.registros())
            ctrl.pln_recibos.gravar()
        elif args.tipo == '1210':
            consultar_s1210(registros=ctrl.pln_recibos.registros())
            ctrl.pln_recibos.gravar()