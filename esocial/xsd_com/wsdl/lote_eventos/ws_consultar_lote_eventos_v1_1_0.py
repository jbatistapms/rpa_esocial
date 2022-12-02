from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/consulta/retornoProcessamento/v1_1_0"


@dataclass
class ConsultarLoteEventos:
    class Meta:
        namespace = "http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/consulta/retornoProcessamento/v1_1_0"

    consulta: Optional["ConsultarLoteEventos.Consulta"] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

    @dataclass
    class Consulta:
        any_element: Optional[object] = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            }
        )


@dataclass
class ConsultarLoteEventosResponse:
    class Meta:
        namespace = "http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/consulta/retornoProcessamento/v1_1_0"

    consultar_lote_eventos_result: Optional["ConsultarLoteEventosResponse.ConsultarLoteEventosResult"] = field(
        default=None,
        metadata={
            "name": "ConsultarLoteEventosResult",
            "type": "Element",
        }
    )

    @dataclass
    class ConsultarLoteEventosResult:
        any_element: Optional[object] = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            }
        )
