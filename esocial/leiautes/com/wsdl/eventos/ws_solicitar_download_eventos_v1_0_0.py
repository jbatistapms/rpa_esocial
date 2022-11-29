from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.esocial.gov.br/servicos/empregador/download/solicitacao/v1_0_0"


@dataclass
class SolicitarDownloadEventosPorId:
    class Meta:
        namespace = "http://www.esocial.gov.br/servicos/empregador/download/solicitacao/v1_0_0"

    solicitacao: Optional["SolicitarDownloadEventosPorId.Solicitacao"] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

    @dataclass
    class Solicitacao:
        any_element: Optional[object] = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            }
        )


@dataclass
class SolicitarDownloadEventosPorIdResponse:
    class Meta:
        namespace = "http://www.esocial.gov.br/servicos/empregador/download/solicitacao/v1_0_0"

    solicitar_download_eventos_por_id_result: Optional["SolicitarDownloadEventosPorIdResponse.SolicitarDownloadEventosPorIdResult"] = field(
        default=None,
        metadata={
            "name": "SolicitarDownloadEventosPorIdResult",
            "type": "Element",
        }
    )

    @dataclass
    class SolicitarDownloadEventosPorIdResult:
        any_element: Optional[object] = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            }
        )


@dataclass
class SolicitarDownloadEventosPorNrRecibo:
    class Meta:
        namespace = "http://www.esocial.gov.br/servicos/empregador/download/solicitacao/v1_0_0"

    solicitacao: Optional["SolicitarDownloadEventosPorNrRecibo.Solicitacao"] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

    @dataclass
    class Solicitacao:
        any_element: Optional[object] = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            }
        )


@dataclass
class SolicitarDownloadEventosPorNrReciboResponse:
    class Meta:
        namespace = "http://www.esocial.gov.br/servicos/empregador/download/solicitacao/v1_0_0"

    solicitar_download_eventos_por_nr_recibo_result: Optional["SolicitarDownloadEventosPorNrReciboResponse.SolicitarDownloadEventosPorNrReciboResult"] = field(
        default=None,
        metadata={
            "name": "SolicitarDownloadEventosPorNrReciboResult",
            "type": "Element",
        }
    )

    @dataclass
    class SolicitarDownloadEventosPorNrReciboResult:
        any_element: Optional[object] = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            }
        )
