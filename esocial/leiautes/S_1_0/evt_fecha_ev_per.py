from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from . import tipos
from .xmldsig_core_schema import Signature

__NAMESPACE__ = "http://www.esocial.gov.br/schema/evt/evtFechaEvPer/v_S_01_00_00"


class InfoFechIndExcApur1250(Enum):
    """Indicativo de exclusão de apuração das aquisições de produção rural
    (eventos S-1250) do período de apuração.

    Validação: Não informar se {perApur}(1299_ideEvento_perApur) &gt;= [2021-07] ou se {indApuracao}(1299_ideEvento_indApuracao) = [2]. Preenchimento obrigatório caso o campo tenha sido informado em fechamento anterior do mesmo período de apuração.

    :cvar S: Sim
    """
    S = "S"


class InfoFechNaoValid(Enum):
    """Indicativo de não validação das regras de fechamento, para que os
    grandes contribuintes possam reduzir o tempo de processamento do evento.

    O preenchimento deste campo implica a não execução da REGRA_VALIDA_FECHAMENTO_FOPAG.
    Validação: Não informar se {procEmi}(1299_ideEvento_procEmi) for diferente de [1].

    :cvar S: Sim
    """
    S = "S"


class InfoFechTransDctfweb(Enum):
    """Solicitação de transmissão imediata da DCTFWeb.

    Validação: Não informar se {perApur}(1299_ideEvento_perApur) &lt; [2021-10]. Preenchimento obrigatório se {perApur}(1299_ideEvento_perApur) &gt;= [2021-10] e ({classTrib}(1000_infoEmpregador_inclusao_infoCadastro_classTrib) em S-1000 = [04] ou {indGuia}(1299_ideEvento_indGuia) estiver informado).

    :cvar S: Sim
    """
    S = "S"


@dataclass
class Evento:
    """S-1299 - Fechamento dos Eventos Periódicos

    :ivar evt_fecha_ev_per: Evento Fechamento dos Eventos Periódicos.
        CHAVE_GRUPO: {Id} REGRA:REGRA_ENVIO_PROC_FECHAMENTO
        REGRA:REGRA_EVE_FOPAG_SIMPLIFICADO
        REGRA:REGRA_EXISTE_INFO_EMPREGADOR
        REGRA:REGRA_REMUN_ANUAL_DEZEMBRO REGRA:REGRA_VALIDA_EMPREGADOR
        REGRA:REGRA_VALIDA_FECHAMENTO_FOPAG
    :ivar signature:
    """
    class Meta:
        name = "eSocial"
        namespace = "http://www.esocial.gov.br/schema/evt/evtFechaEvPer/v_S_01_00_00"
        schema = "esquemas_xsd_s_1_0/evtFechaEvPer.xsd"

    evt_fecha_ev_per: Optional["Evento.EvtFechaEvPer"] = field(
        default=None,
        metadata={
            "name": "evtFechaEvPer",
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
    class EvtFechaEvPer:
        """
        :ivar ide_evento:
        :ivar ide_empregador:
        :ivar info_fech: Informações do fechamento.
        :ivar id:
        """
        ide_evento: Optional[tipos.TIdeEventoFolhaSemRetificacao] = field(
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
        info_fech: Optional["Evento.EvtFechaEvPer.InfoFech"] = field(
            default=None,
            metadata={
                "name": "infoFech",
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
        class InfoFech:
            """
            :ivar evt_remun: Possui informações relativas a remuneração
                de trabalhadores ou provento/pensão de beneficiários no
                período de apuração? Validação: Se for igual a [S], deve
                existir evento de remuneração (S-1200, S-1202, S-1207,
                S-2299 ou S-2399) para o período de apuração,
                considerando o campo {indGuia}(1299_ideEvento_indGuia).
                Caso contrário, não deve existir evento de remuneração.
            :ivar evt_com_prod: Possui informações de comercialização de
                produção? Validação: Se for igual a [S], deve existir o
                evento S-1260 para o período de apuração, considerando o
                campo {indGuia}(1299_ideEvento_indGuia). Caso contrário,
                não deve existir o evento.
            :ivar evt_contrat_av_np: Contratou, por intermédio de
                sindicato, serviços de trabalhadores avulsos não
                portuários? Validação: Se for igual a [S], deve existir
                o evento S-1270 para o período de apuração, considerando
                o campo {indGuia}(1299_ideEvento_indGuia). Caso
                contrário, não deve existir o evento.
            :ivar evt_info_compl_per: Possui informações de desoneração
                de folha de pagamento ou, sendo empresa enquadrada no
                Simples, possui informações sobre a receita obtida em
                atividades cuja contribuição previdenciária incidente
                sobre a folha de pagamento é concomitantemente
                substituída e não substituída? Validação: Se for igual a
                [S], deve existir o evento S-1280 para o período de
                apuração. Caso contrário, não deve existir o evento.
            :ivar ind_exc_apur1250:
            :ivar trans_dctfweb:
            :ivar nao_valid:
            """
            evt_remun: Optional[str] = field(
                default=None,
                metadata={
                    "name": "evtRemun",
                    "type": "Element",
                    "required": True,
                }
            )
            evt_com_prod: Optional[str] = field(
                default=None,
                metadata={
                    "name": "evtComProd",
                    "type": "Element",
                    "required": True,
                }
            )
            evt_contrat_av_np: Optional[str] = field(
                default=None,
                metadata={
                    "name": "evtContratAvNP",
                    "type": "Element",
                    "required": True,
                }
            )
            evt_info_compl_per: Optional[str] = field(
                default=None,
                metadata={
                    "name": "evtInfoComplPer",
                    "type": "Element",
                    "required": True,
                }
            )
            ind_exc_apur1250: Optional[InfoFechIndExcApur1250] = field(
                default=None,
                metadata={
                    "name": "indExcApur1250",
                    "type": "Element",
                }
            )
            trans_dctfweb: Optional[InfoFechTransDctfweb] = field(
                default=None,
                metadata={
                    "name": "transDCTFWeb",
                    "type": "Element",
                }
            )
            nao_valid: Optional[InfoFechNaoValid] = field(
                default=None,
                metadata={
                    "name": "naoValid",
                    "type": "Element",
                }
            )
