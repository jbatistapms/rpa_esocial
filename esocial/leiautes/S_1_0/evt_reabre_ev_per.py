from dataclasses import dataclass, field
from typing import Optional

from . import tipos
from .xmldsig_core_schema import Signature

__NAMESPACE__ = "http://www.esocial.gov.br/schema/evt/evtReabreEvPer/v_S_01_00_00"


@dataclass
class Evento:
    """S-1298 - Reabertura dos Eventos Periódicos

    :ivar evt_reabre_ev_per: Evento Reabertura dos Eventos Periódicos.
        CHAVE_GRUPO: {Id} REGRA:REGRA_ENVIO_PROC_FECHAMENTO
        REGRA:REGRA_EVE_FOPAG_SIMPLIFICADO
        REGRA:REGRA_EXISTE_INFO_EMPREGADOR
        REGRA:REGRA_REABERTURA_VALIDA_PERIODO_APURACAO
        REGRA:REGRA_VALIDA_EMPREGADOR
    :ivar signature:
    """
    class Meta:
        name = "eSocial"
        namespace = "http://www.esocial.gov.br/schema/evt/evtReabreEvPer/v_S_01_00_00"
        schema = "esquemas_xsd_s_1_0/evtReabreEvPer.xsd"

    evt_reabre_ev_per: Optional["Evento.EvtReabreEvPer"] = field(
        default=None,
        metadata={
            "name": "evtReabreEvPer",
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
    class EvtReabreEvPer:
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
        id: Optional[str] = field(
            default=None,
            metadata={
                "name": "Id",
                "type": "Attribute",
                "required": True,
            }
        )
