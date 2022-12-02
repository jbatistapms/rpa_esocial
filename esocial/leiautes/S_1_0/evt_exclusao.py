from dataclasses import dataclass, field
from typing import Optional

from . import tipos
from .xmldsig_core_schema import Signature

__NAMESPACE__ = "http://www.esocial.gov.br/schema/evt/evtExclusao/v_S_01_00_00"


@dataclass
class Evento:
    """S-3000 - Exclusão de Eventos

    :ivar evt_exclusao: Evento Exclusão DESCRICAO_COMPLETA:Evento
        Exclusão de Eventos. CHAVE_GRUPO: {Id}
        REGRA:REGRA_ENVIO_PROC_FECHAMENTO
        REGRA:REGRA_EVE_EXCLUSAO_VALIDA_NRRECIBO
        REGRA:REGRA_EXISTE_INFO_EMPREGADOR REGRA:REGRA_EXTEMP_DOMESTICO
        REGRA:REGRA_MESMO_PROCEMI REGRA:REGRA_VALIDA_EMPREGADOR
    :ivar signature:
    """
    class Meta:
        name = "eSocial"
        namespace = "http://www.esocial.gov.br/schema/evt/evtExclusao/v_S_01_00_00"
        schema = "esquemas_xsd_s_1_0/evtExclusao.xsd"

    evt_exclusao: Optional["Evento.EvtExclusao"] = field(
        default=None,
        metadata={
            "name": "evtExclusao",
            "type": "Element",
            "required": True,
        }
    )
    signature: Optional[Signature] = field(
        default=None,
        metadata={
            "name": "Signature",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "required": True,
        }
    )

    @dataclass
    class EvtExclusao:
        """
        :ivar ide_evento:
        :ivar ide_empregador:
        :ivar info_exclusao: Informação do evento que será excluído
            DESCRICAO_COMPLETA:Grupo que identifica o evento objeto da
            exclusão.
        :ivar id:
        """
        ide_evento: Optional[tipos.TIdeEventoEvtTabInicial] = field(
            default=None,
            metadata={
                "name": "ideEvento",
                "type": "Element",
                "required": True,
            }
        )
        ide_empregador: Optional[tipos.TIdeEmpregador] = field(
            default=None,
            metadata={
                "name": "ideEmpregador",
                "type": "Element",
                "required": True,
            }
        )
        info_exclusao: Optional["Evento.EvtExclusao.InfoExclusao"] = field(
            default=None,
            metadata={
                "name": "infoExclusao",
                "type": "Element",
                "required": True,
            }
        )
        id: Optional[str] = field(
            default=None,
            metadata={
                "name": "Id",
                "type": "Attribute",
                "required": True,
            }
        )

        @dataclass
        class InfoExclusao:
            """
            :ivar tp_evento:
            :ivar nr_rec_evt: Preencher com o número do recibo do evento
                que será excluído. Validação: O recibo deve ser relativo
                ao mesmo tipo de evento indicado em
                {tpEvento}(./tpEvento) e o respectivo evento não deve
                constar como excluído ou retificado. Além disso, no caso
                de exclusão de eventos em que existe a identificação do
                trabalhador, o evento que está sendo excluído deve
                referir-se ao mesmo trabalhador identificado por
                {cpfTrab}(./ideTrabalhador_cpfTrab).
            :ivar ide_trabalhador: Identificação do trabalhador a que se
                refere o evento a ser excluído DESCRICAO_COMPLETA:Grupo
                que identifica a qual trabalhador se refere o evento a
                ser excluído. CONDICAO_GRUPO: O (se
                {tpEvento}(../tpEvento) corresponder a um dos eventos
                não periódicos (S-2190 a S-2420 ou S-8299) ou um dos
                eventos periódicos (S-1200 a S-1210); N (nos demais
                casos)
            :ivar ide_folha_pagto: Identificação do período de apuração
                a que se refere o evento que será excluído
                DESCRICAO_COMPLETA:Grupo que identifica a qual período
                de apuração pertence o evento que será excluído.
                CONDICAO_GRUPO: O (se {tpEvento}(../tpEvento)
                corresponder a um dos eventos periódicos (S-1200 a
                S-1280 ou S-1300)); N (nos demais casos)
            """
            tp_evento: Optional[str] = field(
                default=None,
                metadata={
                    "name": "tpEvento",
                    "type": "Element",
                    "required": True,
                    "length": 6,
                }
            )
            nr_rec_evt: Optional[str] = field(
                default=None,
                metadata={
                    "name": "nrRecEvt",
                    "type": "Element",
                    "required": True,
                }
            )
            ide_trabalhador: Optional["Evento.EvtExclusao.InfoExclusao.IdeTrabalhador"] = field(
                default=None,
                metadata={
                    "name": "ideTrabalhador",
                    "type": "Element",
                }
            )
            ide_folha_pagto: Optional["Evento.EvtExclusao.InfoExclusao.IdeFolhaPagto"] = field(
                default=None,
                metadata={
                    "name": "ideFolhaPagto",
                    "type": "Element",
                }
            )

            @dataclass
            class IdeTrabalhador:
                """
                :ivar cpf_trab: Preencher com o número do CPF do
                    trabalhador ou do beneficiário. Validação: O CPF
                    indicado deve existir na base de dados do RET.
                """
                cpf_trab: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "cpfTrab",
                        "type": "Element",
                        "required": True,
                    }
                )

            @dataclass
            class IdeFolhaPagto:
                """
                :ivar ind_apuracao: Indicativo de período de apuração.
                    Validação: Preenchimento obrigatório e exclusivo se
                    {tpEvento}(../tpEvento) = [S-1200, S-1202, S-1207,
                    S-1280, S-1300].
                :ivar per_apur: Informar o mês/ano (formato AAAA-MM) ou
                    apenas o ano (formato AAAA) de referência das
                    informações. Validação: Deve ser um mês/ano ou ano
                    válido, posterior à implementação do eSocial.
                    Somente pode ser informado ano (formato AAAA) se
                    {indApuracao}(./indApuracao) = [2].
                """
                ind_apuracao: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "indApuracao",
                        "type": "Element",
                    }
                )
                per_apur: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "perApur",
                        "type": "Element",
                        "required": True,
                    }
                )
