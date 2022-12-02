from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

__NAMESPACE__ = "http://www.esocial.gov.br/schema/lote/eventos/envio/v1_1_1"


@dataclass
class TarquivoEsocial:
    """
    Define os dados de um arquivo do eSocial (evento).

    :ivar any_element: Contém o xml do evento.
    :ivar id: Contém a chave de acesso do evento contido no elemento
        xsd:any. É através deste atributo que o empregador conseguirá
        fazer o mapeamento entre o evento que ele enviou e o resultado
        do processamento de cada evento.
    """
    class Meta:
        name = "TArquivoEsocial"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
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


class TideEmpregadorTpInsc(Enum):
    VALUE_1 = 1
    VALUE_2 = 2


class TideTransmissorTpInsc(Enum):
    VALUE_1 = 1
    VALUE_2 = 2


@dataclass
class TideEmpregador:
    """
    Define a identificação do empregador.
    """
    class Meta:
        name = "TIdeEmpregador"

    tp_insc: Optional[TideEmpregadorTpInsc] = field(
        default=None,
        metadata={
            "name": "tpInsc",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/v1_1_1",
            "required": True,
        }
    )
    nr_insc: Optional[str] = field(
        default=None,
        metadata={
            "name": "nrInsc",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/v1_1_1",
            "required": True,
            "pattern": r"\d{8,15}",
        }
    )


@dataclass
class TideTransmissor:
    """
    Define a identificação do transmissor.
    """
    class Meta:
        name = "TIdeTransmissor"

    tp_insc: Optional[TideTransmissorTpInsc] = field(
        default=None,
        metadata={
            "name": "tpInsc",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/v1_1_1",
            "required": True,
        }
    )
    nr_insc: Optional[str] = field(
        default=None,
        metadata={
            "name": "nrInsc",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/v1_1_1",
            "required": True,
            "pattern": r"\d{8,15}",
        }
    )


@dataclass
class ESocial:
    """
    Elemento raiz do eSocial.

    :ivar envio_lote_eventos: Representa um lote de eventos.
    """
    class Meta:
        name = "eSocial"
        namespace = "http://www.esocial.gov.br/schema/lote/eventos/envio/v1_1_1"

    envio_lote_eventos: Optional["ESocial.EnvioLoteEventos"] = field(
        default=None,
        metadata={
            "name": "envioLoteEventos",
            "type": "Element",
            "required": True,
        }
    )

    @dataclass
    class EnvioLoteEventos:
        """
        :ivar ide_empregador: Identificação do empregador.
        :ivar ide_transmissor: Identificação do transmissor.
        :ivar eventos: Contém a relação de eventos que compõe o lote.
        :ivar grupo:
        """
        ide_empregador: Optional[TideEmpregador] = field(
            default=None,
            metadata={
                "name": "ideEmpregador",
                "type": "Element",
                "required": True,
            }
        )
        ide_transmissor: Optional[TideTransmissor] = field(
            default=None,
            metadata={
                "name": "ideTransmissor",
                "type": "Element",
                "required": True,
            }
        )
        eventos: Optional["ESocial.EnvioLoteEventos.Eventos"] = field(
            default=None,
            metadata={
                "type": "Element",
                "required": True,
            }
        )
        grupo: Optional[int] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )

        @dataclass
        class Eventos:
            evento: List[TarquivoEsocial] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "min_occurs": 1,
                }
            )
