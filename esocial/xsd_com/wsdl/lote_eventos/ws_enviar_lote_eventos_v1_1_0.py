from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/v1_1_0"


@dataclass
class EnviarLoteEventos:
    class Meta:
        namespace = "http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/v1_1_0"

    lote_eventos: Optional["EnviarLoteEventos.LoteEventos"] = field(
        default=None,
        metadata={
            "name": "loteEventos",
            "type": "Element",
        }
    )

    @dataclass
    class LoteEventos:
        any_element: Optional[object] = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            }
        )


@dataclass
class EnviarLoteEventosResponse:
    class Meta:
        namespace = "http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/v1_1_0"

    enviar_lote_eventos_result: Optional["EnviarLoteEventosResponse.EnviarLoteEventosResult"] = field(
        default=None,
        metadata={
            "name": "EnviarLoteEventosResult",
            "type": "Element",
        }
    )

    @dataclass
    class EnviarLoteEventosResult:
        any_element: Optional[object] = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            }
        )
