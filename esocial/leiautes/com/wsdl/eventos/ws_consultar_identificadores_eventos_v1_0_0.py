from dataclasses import dataclass, field
from typing import Optional
from xsd_com.wsdl.eventos.ws_solicitar_download_eventos_v1_0_0 import (
    SolicitarDownloadEventosPorId,
    SolicitarDownloadEventosPorIdResponse,
    SolicitarDownloadEventosPorNrRecibo,
    SolicitarDownloadEventosPorNrReciboResponse,
)
from xsd_com.wsdl.lote_eventos.ws_consultar_lote_eventos_v1_1_0 import (
    ConsultarLoteEventos,
    ConsultarLoteEventosResponse,
)
from xsd_com.wsdl.lote_eventos.ws_enviar_lote_eventos_v1_1_0 import (
    EnviarLoteEventos,
    EnviarLoteEventosResponse,
)

__NAMESPACE__ = "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0"


@dataclass
class ConsultarIdentificadoresEventosEmpregador:
    class Meta:
        namespace = "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0"

    consulta_eventos_empregador: Optional["ConsultarIdentificadoresEventosEmpregador.ConsultaEventosEmpregador"] = field(
        default=None,
        metadata={
            "name": "consultaEventosEmpregador",
            "type": "Element",
        }
    )

    @dataclass
    class ConsultaEventosEmpregador:
        any_element: Optional[object] = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            }
        )


@dataclass
class ConsultarIdentificadoresEventosEmpregadorResponse:
    class Meta:
        namespace = "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0"

    consultar_identificadores_eventos_empregador_result: Optional["ConsultarIdentificadoresEventosEmpregadorResponse.ConsultarIdentificadoresEventosEmpregadorResult"] = field(
        default=None,
        metadata={
            "name": "ConsultarIdentificadoresEventosEmpregadorResult",
            "type": "Element",
        }
    )

    @dataclass
    class ConsultarIdentificadoresEventosEmpregadorResult:
        any_element: Optional[object] = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            }
        )


@dataclass
class ConsultarIdentificadoresEventosTabela:
    class Meta:
        namespace = "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0"

    consulta_eventos_tabela: Optional["ConsultarIdentificadoresEventosTabela.ConsultaEventosTabela"] = field(
        default=None,
        metadata={
            "name": "consultaEventosTabela",
            "type": "Element",
        }
    )

    @dataclass
    class ConsultaEventosTabela:
        any_element: Optional[object] = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            }
        )


@dataclass
class ConsultarIdentificadoresEventosTabelaResponse:
    class Meta:
        namespace = "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0"

    consultar_identificadores_eventos_tabela_result: Optional["ConsultarIdentificadoresEventosTabelaResponse.ConsultarIdentificadoresEventosTabelaResult"] = field(
        default=None,
        metadata={
            "name": "ConsultarIdentificadoresEventosTabelaResult",
            "type": "Element",
        }
    )

    @dataclass
    class ConsultarIdentificadoresEventosTabelaResult:
        any_element: Optional[object] = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            }
        )


@dataclass
class ConsultarIdentificadoresEventosTrabalhador:
    class Meta:
        namespace = "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0"

    consulta_eventos_trabalhador: Optional["ConsultarIdentificadoresEventosTrabalhador.ConsultaEventosTrabalhador"] = field(
        default=None,
        metadata={
            "name": "consultaEventosTrabalhador",
            "type": "Element",
        }
    )

    @dataclass
    class ConsultaEventosTrabalhador:
        any_element: Optional[object] = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            }
        )


@dataclass
class ConsultarIdentificadoresEventosTrabalhadorResponse:
    class Meta:
        namespace = "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0"

    consultar_identificadores_eventos_trabalhador_result: Optional["ConsultarIdentificadoresEventosTrabalhadorResponse.ConsultarIdentificadoresEventosTrabalhadorResult"] = field(
        default=None,
        metadata={
            "name": "ConsultarIdentificadoresEventosTrabalhadorResult",
            "type": "Element",
        }
    )

    @dataclass
    class ConsultarIdentificadoresEventosTrabalhadorResult:
        any_element: Optional[object] = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            }
        )


@dataclass
class ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosEmpregadorInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    body: Optional["ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosEmpregadorInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        }
    )

    @dataclass
    class Body:
        consultar_identificadores_eventos_empregador: Optional[ConsultarIdentificadoresEventosEmpregador] = field(
            default=None,
            metadata={
                "name": "ConsultarIdentificadoresEventosEmpregador",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0",
            }
        )


@dataclass
class ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosEmpregadorOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    body: Optional["ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosEmpregadorOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        }
    )

    @dataclass
    class Body:
        consultar_identificadores_eventos_empregador_response: Optional[ConsultarIdentificadoresEventosEmpregadorResponse] = field(
            default=None,
            metadata={
                "name": "ConsultarIdentificadoresEventosEmpregadorResponse",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0",
            }
        )
        fault: Optional["ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosEmpregadorOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            }
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            detail: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )


@dataclass
class ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTabelaInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    body: Optional["ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTabelaInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        }
    )

    @dataclass
    class Body:
        consultar_identificadores_eventos_tabela: Optional[ConsultarIdentificadoresEventosTabela] = field(
            default=None,
            metadata={
                "name": "ConsultarIdentificadoresEventosTabela",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0",
            }
        )


@dataclass
class ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTabelaOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    body: Optional["ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTabelaOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        }
    )

    @dataclass
    class Body:
        consultar_identificadores_eventos_tabela_response: Optional[ConsultarIdentificadoresEventosTabelaResponse] = field(
            default=None,
            metadata={
                "name": "ConsultarIdentificadoresEventosTabelaResponse",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0",
            }
        )
        fault: Optional["ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTabelaOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            }
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            detail: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )


@dataclass
class ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTrabalhadorInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    body: Optional["ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTrabalhadorInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        }
    )

    @dataclass
    class Body:
        consultar_identificadores_eventos_trabalhador: Optional[ConsultarIdentificadoresEventosTrabalhador] = field(
            default=None,
            metadata={
                "name": "ConsultarIdentificadoresEventosTrabalhador",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0",
            }
        )


@dataclass
class ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTrabalhadorOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    body: Optional["ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTrabalhadorOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        }
    )

    @dataclass
    class Body:
        consultar_identificadores_eventos_trabalhador_response: Optional[ConsultarIdentificadoresEventosTrabalhadorResponse] = field(
            default=None,
            metadata={
                "name": "ConsultarIdentificadoresEventosTrabalhadorResponse",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0",
            }
        )
        fault: Optional["ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTrabalhadorOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            }
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            detail: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )


@dataclass
class ServicoConsultarLoteEventosConsultarLoteEventosInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    body: Optional["ServicoConsultarLoteEventosConsultarLoteEventosInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        }
    )

    @dataclass
    class Body:
        consultar_lote_eventos: Optional[ConsultarLoteEventos] = field(
            default=None,
            metadata={
                "name": "ConsultarLoteEventos",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/consulta/retornoProcessamento/v1_1_0",
            }
        )


@dataclass
class ServicoConsultarLoteEventosConsultarLoteEventosOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    body: Optional["ServicoConsultarLoteEventosConsultarLoteEventosOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        }
    )

    @dataclass
    class Body:
        consultar_lote_eventos_response: Optional[ConsultarLoteEventosResponse] = field(
            default=None,
            metadata={
                "name": "ConsultarLoteEventosResponse",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/consulta/retornoProcessamento/v1_1_0",
            }
        )
        fault: Optional["ServicoConsultarLoteEventosConsultarLoteEventosOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            }
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            detail: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )


@dataclass
class ServicoEnviarLoteEventosEnviarLoteEventosInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    body: Optional["ServicoEnviarLoteEventosEnviarLoteEventosInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        }
    )

    @dataclass
    class Body:
        enviar_lote_eventos: Optional[EnviarLoteEventos] = field(
            default=None,
            metadata={
                "name": "EnviarLoteEventos",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/v1_1_0",
            }
        )


@dataclass
class ServicoEnviarLoteEventosEnviarLoteEventosOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    body: Optional["ServicoEnviarLoteEventosEnviarLoteEventosOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        }
    )

    @dataclass
    class Body:
        enviar_lote_eventos_response: Optional[EnviarLoteEventosResponse] = field(
            default=None,
            metadata={
                "name": "EnviarLoteEventosResponse",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/v1_1_0",
            }
        )
        fault: Optional["ServicoEnviarLoteEventosEnviarLoteEventosOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            }
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            detail: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )


@dataclass
class ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorIdInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    body: Optional["ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorIdInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        }
    )

    @dataclass
    class Body:
        solicitar_download_eventos_por_id: Optional[SolicitarDownloadEventosPorId] = field(
            default=None,
            metadata={
                "name": "SolicitarDownloadEventosPorId",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/servicos/empregador/download/solicitacao/v1_0_0",
            }
        )


@dataclass
class ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorIdOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    body: Optional["ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorIdOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        }
    )

    @dataclass
    class Body:
        solicitar_download_eventos_por_id_response: Optional[SolicitarDownloadEventosPorIdResponse] = field(
            default=None,
            metadata={
                "name": "SolicitarDownloadEventosPorIdResponse",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/servicos/empregador/download/solicitacao/v1_0_0",
            }
        )
        fault: Optional["ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorIdOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            }
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            detail: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )


@dataclass
class ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorNrReciboInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    body: Optional["ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorNrReciboInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        }
    )

    @dataclass
    class Body:
        solicitar_download_eventos_por_nr_recibo: Optional[SolicitarDownloadEventosPorNrRecibo] = field(
            default=None,
            metadata={
                "name": "SolicitarDownloadEventosPorNrRecibo",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/servicos/empregador/download/solicitacao/v1_0_0",
            }
        )


@dataclass
class ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorNrReciboOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    body: Optional["ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorNrReciboOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        }
    )

    @dataclass
    class Body:
        solicitar_download_eventos_por_nr_recibo_response: Optional[SolicitarDownloadEventosPorNrReciboResponse] = field(
            default=None,
            metadata={
                "name": "SolicitarDownloadEventosPorNrReciboResponse",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/servicos/empregador/download/solicitacao/v1_0_0",
            }
        )
        fault: Optional["ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorNrReciboOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            }
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            detail: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )


class ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosEmpregador:
    uri = "#BasicHttpBinding_ServicoConsultarIdentificadoresEventos_policy"
    style = "document"
    location = "endereco_ambiente_acessar_consulta"
    transport = "http://schemas.xmlsoap.org/soap/http"
    soap_action = "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0/ServicoConsultarIdentificadoresEventos/ConsultarIdentificadoresEventosEmpregador"
    input = ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosEmpregadorInput
    output = ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosEmpregadorOutput


class ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTabela:
    uri = "#BasicHttpBinding_ServicoConsultarIdentificadoresEventos_policy"
    style = "document"
    location = "endereco_ambiente_acessar_consulta"
    transport = "http://schemas.xmlsoap.org/soap/http"
    soap_action = "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0/ServicoConsultarIdentificadoresEventos/ConsultarIdentificadoresEventosTabela"
    input = ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTabelaInput
    output = ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTabelaOutput


class ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTrabalhador:
    uri = "#BasicHttpBinding_ServicoConsultarIdentificadoresEventos_policy"
    style = "document"
    location = "endereco_ambiente_acessar_consulta"
    transport = "http://schemas.xmlsoap.org/soap/http"
    soap_action = "http://www.esocial.gov.br/servicos/empregador/consulta/identificadores-eventos/v1_0_0/ServicoConsultarIdentificadoresEventos/ConsultarIdentificadoresEventosTrabalhador"
    input = ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTrabalhadorInput
    output = ServicoConsultarIdentificadoresEventosConsultarIdentificadoresEventosTrabalhadorOutput


class ServicoConsultarLoteEventosConsultarLoteEventos:
    uri = "#Servicos.Empregador_ServicoConsultarLoteEventos_policy"
    style = "document"
    location = "endereco_ambiente_acessar_consulta"
    transport = "http://schemas.xmlsoap.org/soap/http"
    soap_action = "http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/consulta/retornoProcessamento/v1_1_0/ServicoConsultarLoteEventos/ConsultarLoteEventos"
    input = ServicoConsultarLoteEventosConsultarLoteEventosInput
    output = ServicoConsultarLoteEventosConsultarLoteEventosOutput


class ServicoEnviarLoteEventosEnviarLoteEventos:
    uri = "#WsEnviarLoteEventos_policy"
    style = "document"
    location = "endereco_ambiente_acessar_envio"
    transport = "http://schemas.xmlsoap.org/soap/http"
    soap_action = "http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/v1_1_0/ServicoEnviarLoteEventos/EnviarLoteEventos"
    input = ServicoEnviarLoteEventosEnviarLoteEventosInput
    output = ServicoEnviarLoteEventosEnviarLoteEventosOutput


class ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorId:
    uri = "#ServicoSolicitarDownloadEventos_policy"
    style = "document"
    location = "endereco_ambiente_acessar_consulta"
    transport = "http://schemas.xmlsoap.org/soap/http"
    soap_action = "http://www.esocial.gov.br/servicos/empregador/download/solicitacao/v1_0_0/ServicoSolicitarDownloadEventos/SolicitarDownloadEventosPorId"
    input = ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorIdInput
    output = ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorIdOutput


class ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorNrRecibo:
    uri = "#ServicoSolicitarDownloadEventos_policy"
    style = "document"
    location = "endereco_ambiente_acessar_consulta"
    transport = "http://schemas.xmlsoap.org/soap/http"
    soap_action = "http://www.esocial.gov.br/servicos/empregador/download/solicitacao/v1_0_0/ServicoSolicitarDownloadEventos/SolicitarDownloadEventosPorNrRecibo"
    input = ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorNrReciboInput
    output = ServicoSolicitarDownloadEventosSolicitarDownloadEventosPorNrReciboOutput
