from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from xsd_com.xsd.eventos.solicitacao_download_eventos.xmldsig_core_schema import Signature

__NAMESPACE__ = "http://www.esocial.gov.br/schema/consulta/identificadores-eventos/trabalhador/v1_0_0"


@dataclass
class TconsultaEventosTrabalhador:
    """
    Define o filtro para consulta aos eventos de trabalhador.
    """
    class Meta:
        name = "TConsultaEventosTrabalhador"

    cpf_trab: Optional[str] = field(
        default=None,
        metadata={
            "name": "cpfTrab",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/consulta/identificadores-eventos/trabalhador/v1_0_0",
            "required": True,
            "length": 11,
            "pattern": r"\d{11}",
        }
    )
    dt_ini: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "dtIni",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/consulta/identificadores-eventos/trabalhador/v1_0_0",
            "required": True,
        }
    )
    dt_fim: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "dtFim",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/consulta/identificadores-eventos/trabalhador/v1_0_0",
            "required": True,
        }
    )


class TideEmpregadorTpInsc(Enum):
    """Tipo de empregador.

    1-CNPJ; 2-CPF;
    """
    VALUE_1 = 1
    VALUE_2 = 2


@dataclass
class TideEmpregador:
    """Define a identificação do empregador.

    1-CNPJ; 2-CPF;
    """
    class Meta:
        name = "TIdeEmpregador"

    tp_insc: Optional[TideEmpregadorTpInsc] = field(
        default=None,
        metadata={
            "name": "tpInsc",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/consulta/identificadores-eventos/trabalhador/v1_0_0",
            "required": True,
        }
    )
    nr_insc: Optional[str] = field(
        default=None,
        metadata={
            "name": "nrInsc",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/consulta/identificadores-eventos/trabalhador/v1_0_0",
            "required": True,
            "pattern": r"\d{8,15}",
        }
    )


@dataclass
class ESocial:
    """
    Elemento raiz do eSocial.

    :ivar consulta_identificadores_evts: Elemento de  informacoes
        relativas a consulta de eventos.
    :ivar signature:
    """
    class Meta:
        name = "eSocial"
        namespace = "http://www.esocial.gov.br/schema/consulta/identificadores-eventos/trabalhador/v1_0_0"

    consulta_identificadores_evts: Optional["ESocial.ConsultaIdentificadoresEvts"] = field(
        default=None,
        metadata={
            "name": "consultaIdentificadoresEvts",
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
    class ConsultaIdentificadoresEvts:
        """
        :ivar ide_empregador: Identificação do empregador.
        :ivar consulta_evts_trabalhador: Contém o filtro para consulta
            aos eventos de trabalhador.
        """
        ide_empregador: Optional[TideEmpregador] = field(
            default=None,
            metadata={
                "name": "ideEmpregador",
                "type": "Element",
                "required": True,
            }
        )
        consulta_evts_trabalhador: Optional[TconsultaEventosTrabalhador] = field(
            default=None,
            metadata={
                "name": "consultaEvtsTrabalhador",
                "type": "Element",
                "required": True,
            }
        )
