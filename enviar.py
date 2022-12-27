import sys

from loguru import logger

from coletar import Controlador, destino
from core import args
from esocial import core as core_esocial
from esocial.eventos import *
from esocial.planilhas import *
from esocial.utils import TipoAmbiente

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
        elif args.tipo == '1298':
            enviar_s1298()
        elif args.tipo == '1299':
            enviar_s1299()
        elif args.tipo == '3000':
            pln = PlanilhaS3000()
            enviar_s3000(registros=pln.registros())
            pln.gravar()
    elif args.consulta:
        if args.tipo == '1200':
            consultar_s1200(registros=ctrl.pln_recibos.registros())
            ctrl.pln_recibos.gravar()
        elif args.tipo == '1210':
            consultar_s1210(registros=ctrl.pln_recibos.registros())
            ctrl.pln_recibos.gravar()
        elif args.tipo == '1298':
            consultar_s1298()
        elif args.tipo == '1299':
            consultar_s1299()
        elif args.tipo == '3000':
            pln = PlanilhaS3000()
            consultar_s3000(registros=pln.registros())
            pln.gravar()