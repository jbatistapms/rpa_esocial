from dataclasses import dataclass, field
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0"


@dataclass
class TdadosRecepcao:
    """
    Define os dados de recepção de um arquivo (lote ou evento).

    :ivar dh_recepcao: Data hora recepção.
    :ivar versao_aplicativo_recepcao: Versão do aplicativo de recepção.
    :ivar protocolo_envio: Código de retorno para localização do lote.
        Número sequencial único produzido no instante de recepção da
        mensagem originada no empregador. São válidos os seguintes
        intervalos, expressos na base decimal: A.B.NNNNNNNNNNNNNNNNNNN A
        = Agente de recepção: Serpro=1 ou Caixa=2 (1 posição) B =
        Ambiente de recepção: Produção=1; Pré-produção - dados reais=2;
        Pré-produção - dados fictícios=3; Homologação=6; Validação=7;
        Testes=8; Desenvolvimento=9 N = Número sequencial (19 posições)
        Exemplo: SERPRO: 1.1.0000000000000000001 Caixa:
        2.1.0000000000000000001
    """
    class Meta:
        name = "TDadosRecepcao"

    dh_recepcao: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "dhRecepcao",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0",
            "required": True,
        }
    )
    versao_aplicativo_recepcao: Optional[str] = field(
        default=None,
        metadata={
            "name": "versaoAplicativoRecepcao",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0",
            "required": True,
            "max_length": 30,
        }
    )
    protocolo_envio: Optional[str] = field(
        default=None,
        metadata={
            "name": "protocoloEnvio",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0",
            "required": True,
            "max_length": 30,
        }
    )


@dataclass
class TideEmpregador:
    """
    Define a identificação do empregador.
    """
    class Meta:
        name = "TIdeEmpregador"

    tp_insc: Optional[int] = field(
        default=None,
        metadata={
            "name": "tpInsc",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0",
            "required": True,
        }
    )
    nr_insc: Optional[str] = field(
        default=None,
        metadata={
            "name": "nrInsc",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0",
            "required": True,
            "max_length": 15,
        }
    )


@dataclass
class TideTransmissor:
    """
    Define a identificação do transmissor.
    """
    class Meta:
        name = "TIdeTransmissor"

    tp_insc: Optional[int] = field(
        default=None,
        metadata={
            "name": "tpInsc",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0",
            "required": True,
        }
    )
    nr_insc: Optional[str] = field(
        default=None,
        metadata={
            "name": "nrInsc",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0",
            "required": True,
            "max_length": 15,
        }
    )


@dataclass
class Tocorrencias:
    """
    Define uma ocorrência encontrada no processamento de um arquivo.
    """
    class Meta:
        name = "TOcorrencias"

    ocorrencia: List["Tocorrencias.Ocorrencia"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0",
            "min_occurs": 1,
        }
    )

    @dataclass
    class Ocorrencia:
        """
        :ivar codigo: Código da ocorrência
        :ivar descricao: Descrição da ocorrência
        :ivar tipo: Contém o tipo da ocorrência: 1 - Erro, 2 -
            Advertência
        :ivar localizacao: Contém o caminho do registro e/ou campo em
            que ocorreu o erro.
        """
        codigo: Optional[int] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0",
                "required": True,
            }
        )
        descricao: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0",
                "required": True,
                "max_length": 2048,
            }
        )
        tipo: Optional[int] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0",
                "required": True,
            }
        )
        localizacao: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0",
                "max_length": 2048,
            }
        )


@dataclass
class Tstatus:
    """
    Contém o status atual do lote ou do Evento.

    :ivar cd_resposta: Código de resposta da recepção do lote.
    :ivar desc_resposta: Contém a descrição correspondente ao código de
        resposta.
    :ivar ocorrencias: Contém as ocorrências encontradas durante a
        validação do evento.
    """
    class Meta:
        name = "TStatus"

    cd_resposta: Optional[int] = field(
        default=None,
        metadata={
            "name": "cdResposta",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0",
            "required": True,
        }
    )
    desc_resposta: Optional[str] = field(
        default=None,
        metadata={
            "name": "descResposta",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0",
            "required": True,
            "max_length": 2048,
        }
    )
    ocorrencias: Optional[Tocorrencias] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0",
        }
    )


@dataclass
class ESocial:
    """
    Elemento raiz do eSocial.

    :ivar retorno_envio_lote_eventos: Xml que contém o retorno do
        processo de recepção do lote de eventos.
    """
    class Meta:
        name = "eSocial"
        namespace = "http://www.esocial.gov.br/schema/lote/eventos/envio/retornoEnvio/v1_1_0"

    retorno_envio_lote_eventos: Optional["ESocial.RetornoEnvioLoteEventos"] = field(
        default=None,
        metadata={
            "name": "retornoEnvioLoteEventos",
            "type": "Element",
            "required": True,
        }
    )

    @dataclass
    class RetornoEnvioLoteEventos:
        """
        :ivar ide_empregador: Identificação do empregador.
        :ivar ide_transmissor: Identificação do transmissor.
        :ivar status: Contém o status atual do lote.
        :ivar dados_recepcao_lote: Contém os dados de recepção do lote.
        """
        ide_empregador: Optional[TideEmpregador] = field(
            default=None,
            metadata={
                "name": "ideEmpregador",
                "type": "Element",
            }
        )
        ide_transmissor: Optional[TideTransmissor] = field(
            default=None,
            metadata={
                "name": "ideTransmissor",
                "type": "Element",
            }
        )
        status: Optional[Tstatus] = field(
            default=None,
            metadata={
                "type": "Element",
                "required": True,
            }
        )
        dados_recepcao_lote: Optional[TdadosRecepcao] = field(
            default=None,
            metadata={
                "name": "dadosRecepcaoLote",
                "type": "Element",
            }
        )
