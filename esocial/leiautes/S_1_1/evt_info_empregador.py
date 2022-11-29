from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from xsdata.models.datatype import XmlDate
from .tipos import TIdeEventoEvtTabInicial
from .xmldsig_core_schema import Signature

__NAMESPACE__ = "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00"


@dataclass
class TIdePeriodo:
    """Período de validade das informações.

    CHAVE_GRUPO: {iniValid*}, {fimValid*}
    """
    class Meta:
        name = "T_idePeriodo"

    ini_valid: Optional[str] = field(
        default=None,
        metadata={
            "name": "iniValid",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
            "required": True,
        }
    )
    fim_valid: Optional[str] = field(
        default=None,
        metadata={
            "name": "fimValid",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
        }
    )


class TInfoCadastroIndDesFolha(Enum):
    """Indicativo de desoneração da folha.

    Validação: Pode ser igual a [1] apenas se {classTrib}(./classTrib) = [02, 03, 99]. Nos demais casos, deve ser igual a [0].

    :cvar VALUE_0: Não aplicável
    :cvar VALUE_1: Empresa enquadrada nos arts. 7º a 9º da Lei
        12.546/2011
    """
    VALUE_0 = 0
    VALUE_1 = 1


class TInfoCadastroIndOpcCp(Enum):
    """Indicativo da opção pelo produtor rural pela forma de tributação da
    contribuição previdenciária, nos termos do art.

    25, § 13, da Lei 8.212/1991 e do art. 25, § 7°, da Lei 8.870/1994. O não preenchimento deste campo por parte do produtor rural implica opção pela comercialização da sua produção.
    Validação: Não preencher se {classTrib}(./classTrib) for diferente de [07, 21].

    :cvar VALUE_1: Sobre a comercialização da sua produção
    :cvar VALUE_2: Sobre a folha de pagamento
    """
    VALUE_1 = 1
    VALUE_2 = 2


class TInfoCadastroIndOptRegEletron(Enum):
    """Indica se houve opção pelo registro eletrônico de empregados.

    Caso o declarante seja órgão público sem empregados regidos pela
    CLT, informar [0].

    :cvar VALUE_0: Não optou pelo registro eletrônico de empregados (ou
        opção não aplicável)
    :cvar VALUE_1: Optou pelo registro eletrônico de empregados
    """
    VALUE_0 = 0
    VALUE_1 = 1


class TInfoCadastroIndPorte(Enum):
    """Indicativo de microempresa - ME ou empresa de pequeno porte - EPP para permissão de acesso ao módulo simplificado. Não preencher caso o empregador não se enquadre como micro ou pequena empresa.
    Validação: Não preencher se {classTrib}(./classTrib) = [21, 22].

    :cvar S: Sim
    """
    S = "S"


class TInfoCadastroIndTribFolhaPisCofins(Enum):
    """Indicador de tributação sobre a folha de pagamento - PIS e COFINS.
    Preenchimento exclusivo para o empregador em situação de tributação de PIS e COFINS sobre a folha de pagamento.

    :cvar S: Sim
    """
    S = "S"


class InfoOrgInternacionalIndAcordoIsenMulta(Enum):
    """
    Indicativo da existência de acordo internacional para isenção de multa.

    :cvar VALUE_0: Sem acordo
    :cvar VALUE_1: Com acordo
    """
    VALUE_0 = 0
    VALUE_1 = 1


@dataclass
class TInfoCadastro:
    """
    Detalhamento das informações do empregador.

    :ivar class_trib:
    :ivar ind_coop: Indicativo de cooperativa. Validação: O
        preenchimento do campo é exclusivo e obrigatório para PJ.
        Somente pode ser diferente de [0] se a natureza jurídica do
        declarante for igual a 214-3.
    :ivar ind_constr: Indicativo de construtora. Validação: O
        preenchimento do campo é exclusivo e obrigatório para PJ.
    :ivar ind_des_folha:
    :ivar ind_opc_cp:
    :ivar ind_porte:
    :ivar ind_opt_reg_eletron:
    :ivar cnpj_efr: CNPJ do Ente Federativo Responsável - EFR.
        Validação: Preenchimento obrigatório e exclusivo se a natureza
        jurídica do declarante for Administração Pública (grupo [1]).
        Nesse caso, informar o campo com 14 (catorze) algarismos.
        Informação validada no cadastro do CNPJ da RFB.
    :ivar dt_trans11096: Data da transformação em sociedade de fins
        lucrativos - Lei 11.096/2005. Validação: Não preencher se
        {classTrib}(./classTrib) = [21, 22].
    :ivar ind_trib_folha_pis_cofins:
    :ivar dados_isencao: Informações complementares - Empresas isentas -
        Dados da isenção. CONDICAO_GRUPO: OC (se
        {classTrib}(1000_infoEmpregador_inclusao_infoCadastro_classTrib)
        = [80]); N (nos demais casos)
    :ivar info_org_internacional: Informações exclusivas de organismos
        internacionais e outras instituições extraterritoriais.
        CONDICAO_GRUPO: O (se a natureza jurídica pertencer ao grupo
        [5]); N (nos demais casos)
    """
    class Meta:
        name = "T_infoCadastro"

    class_trib: Optional[str] = field(
        default=None,
        metadata={
            "name": "classTrib",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
            "required": True,
            "pattern": r"\d{2}",
        }
    )
    ind_coop: Optional[str] = field(
        default=None,
        metadata={
            "name": "indCoop",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
        }
    )
    ind_constr: Optional[str] = field(
        default=None,
        metadata={
            "name": "indConstr",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
        }
    )
    ind_des_folha: Optional[TInfoCadastroIndDesFolha] = field(
        default=None,
        metadata={
            "name": "indDesFolha",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
            "required": True,
        }
    )
    ind_opc_cp: Optional[TInfoCadastroIndOpcCp] = field(
        default=None,
        metadata={
            "name": "indOpcCP",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
        }
    )
    ind_porte: Optional[TInfoCadastroIndPorte] = field(
        default=None,
        metadata={
            "name": "indPorte",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
        }
    )
    ind_opt_reg_eletron: Optional[TInfoCadastroIndOptRegEletron] = field(
        default=None,
        metadata={
            "name": "indOptRegEletron",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
            "required": True,
        }
    )
    cnpj_efr: Optional[str] = field(
        default=None,
        metadata={
            "name": "cnpjEFR",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
        }
    )
    dt_trans11096: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "dtTrans11096",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
        }
    )
    ind_trib_folha_pis_cofins: Optional[TInfoCadastroIndTribFolhaPisCofins] = field(
        default=None,
        metadata={
            "name": "indTribFolhaPisCofins",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
        }
    )
    dados_isencao: Optional["TInfoCadastro.DadosIsencao"] = field(
        default=None,
        metadata={
            "name": "dadosIsencao",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
        }
    )
    info_org_internacional: Optional["TInfoCadastro.InfoOrgInternacional"] = field(
        default=None,
        metadata={
            "name": "infoOrgInternacional",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
        }
    )

    @dataclass
    class DadosIsencao:
        """
        :ivar ide_min_lei:
        :ivar nr_certif:
        :ivar dt_emis_certif: Data de emissão do certificado/publicação
            da lei.
        :ivar dt_venc_certif: Data de vencimento do certificado.
            Validação: Não pode ser anterior a
            {dtEmisCertif}(./dtEmisCertif).
        :ivar nr_prot_renov:
        :ivar dt_prot_renov: Data do protocolo de renovação.
        :ivar dt_dou: Data de publicação no Diário Oficial da União -
            DOU.
        :ivar pag_dou:
        """
        ide_min_lei: Optional[str] = field(
            default=None,
            metadata={
                "name": "ideMinLei",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
                "required": True,
                "min_length": 1,
                "max_length": 70,
                "pattern": r".*[^\s].*",
            }
        )
        nr_certif: Optional[str] = field(
            default=None,
            metadata={
                "name": "nrCertif",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
                "required": True,
                "min_length": 1,
                "max_length": 40,
                "pattern": r".*[^\s].*",
            }
        )
        dt_emis_certif: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "dtEmisCertif",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
                "required": True,
            }
        )
        dt_venc_certif: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "dtVencCertif",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
                "required": True,
            }
        )
        nr_prot_renov: Optional[str] = field(
            default=None,
            metadata={
                "name": "nrProtRenov",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
                "min_length": 1,
                "max_length": 40,
                "pattern": r".*[^\s].*",
            }
        )
        dt_prot_renov: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "dtProtRenov",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
            }
        )
        dt_dou: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "dtDou",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
            }
        )
        pag_dou: Optional[str] = field(
            default=None,
            metadata={
                "name": "pagDou",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
                "pattern": r"\d{1,5}",
            }
        )

    @dataclass
    class InfoOrgInternacional:
        ind_acordo_isen_multa: Optional[InfoOrgInternacionalIndAcordoIsenMulta] = field(
            default=None,
            metadata={
                "name": "indAcordoIsenMulta",
                "type": "Element",
                "namespace": "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00",
                "required": True,
            }
        )


@dataclass
class Evento:
    """S-1000 - Informações do Empregador/Contribuinte/Órgão Público

    :ivar evt_info_empregador: Evento Informações do Empregador.
        CHAVE_GRUPO: {Id} REGRA:REGRA_ENVIO_PROC_FECHAMENTO
        REGRA:REGRA_INFO_EMP_PERIODO_CONFLITANTE
        REGRA:REGRA_INFO_EMP_VALIDA_CLASSTRIB_NATJURID
        REGRA:REGRA_INFO_EMP_VALIDA_DTINICIAL
        REGRA:REGRA_TAB_PERMITE_EXCLUSAO REGRA:REGRA_VALIDA_DT_FUTURA
        REGRA:REGRA_VALIDA_EMPREGADOR
    :ivar signature:
    """
    class Meta:
        name = "eSocial"
        namespace = "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v_S_01_01_00"
        schema = "esquemas_xsd_s_1_1/evtInfoEmpregador.xsd"

    evt_info_empregador: Optional["Evento.EvtInfoEmpregador"] = field(
        default=None,
        metadata={
            "name": "evtInfoEmpregador",
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
    class EvtInfoEmpregador:
        """
        :ivar ide_evento:
        :ivar ide_empregador: Informações de identificação do
            empregador. CHAVE_GRUPO: {tpInsc*}, {nrInsc*}
        :ivar info_empregador: Informações do empregador.
            DESCRICAO_COMPLETA:Identificação da operação (inclusão,
            alteração ou exclusão) e das respectivas informações do
            empregador.
        :ivar id:
        """
        ide_evento: Optional[TIdeEventoEvtTabInicial] = field(
            default=None,
            metadata={
                "name": "ideEvento",
                "type": "Element",
                "required": True,
            }
        )
        ide_empregador: Optional["Evento.EvtInfoEmpregador.IdeEmpregador"] = field(
            default=None,
            metadata={
                "name": "ideEmpregador",
                "type": "Element",
                "required": True,
            }
        )
        info_empregador: Optional["Evento.EvtInfoEmpregador.InfoEmpregador"] = field(
            default=None,
            metadata={
                "name": "infoEmpregador",
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
        class IdeEmpregador:
            """
            :ivar tp_insc:
            :ivar nr_insc: Informar o número de inscrição do
                contribuinte de acordo com o tipo de inscrição indicado
                no campo {tpInsc}(./tpInsc). Validação: Se
                {tpInsc}(./tpInsc) for igual a [1], deve ser um número
                de CNPJ válido. Neste caso, deve ser informada apenas a
                raiz/base (8 posições), exceto se a natureza jurídica do
                declarante for igual a 101-5, 104-0, 107-4, 116-3 ou
                134-1, situação em que o campo deve ser preenchido com o
                CNPJ completo (14 posições). Se {tpInsc}(./tpInsc) for
                igual a [2], deve ser um CPF válido.
            """
            tp_insc: Optional[str] = field(
                default=None,
                metadata={
                    "name": "tpInsc",
                    "type": "Element",
                    "required": True,
                }
            )
            nr_insc: Optional[str] = field(
                default=None,
                metadata={
                    "name": "nrInsc",
                    "type": "Element",
                    "required": True,
                }
            )

        @dataclass
        class InfoEmpregador:
            """
            :ivar inclusao: Inclusão de novas informações.
                CONDICAO_GRUPO: OC
            :ivar alteracao: Alteração das informações. CONDICAO_GRUPO:
                OC
            :ivar exclusao: Exclusão das informações. CONDICAO_GRUPO: OC
            """
            inclusao: Optional["Evento.EvtInfoEmpregador.InfoEmpregador.Inclusao"] = field(
                default=None,
                metadata={
                    "type": "Element",
                }
            )
            alteracao: Optional["Evento.EvtInfoEmpregador.InfoEmpregador.Alteracao"] = field(
                default=None,
                metadata={
                    "type": "Element",
                }
            )
            exclusao: Optional["Evento.EvtInfoEmpregador.InfoEmpregador.Exclusao"] = field(
                default=None,
                metadata={
                    "type": "Element",
                }
            )

            @dataclass
            class Inclusao:
                ide_periodo: Optional[TIdePeriodo] = field(
                    default=None,
                    metadata={
                        "name": "idePeriodo",
                        "type": "Element",
                        "required": True,
                    }
                )
                info_cadastro: Optional[TInfoCadastro] = field(
                    default=None,
                    metadata={
                        "name": "infoCadastro",
                        "type": "Element",
                        "required": True,
                    }
                )

            @dataclass
            class Alteracao:
                """
                :ivar ide_periodo:
                :ivar info_cadastro:
                :ivar nova_validade: Novo período de validade das
                    informações. DESCRICAO_COMPLETA:Informação
                    preenchida exclusivamente em caso de alteração do
                    período de validade das informações, apresentando o
                    novo período de validade. CONDICAO_GRUPO: OC
                """
                ide_periodo: Optional[TIdePeriodo] = field(
                    default=None,
                    metadata={
                        "name": "idePeriodo",
                        "type": "Element",
                        "required": True,
                    }
                )
                info_cadastro: Optional[TInfoCadastro] = field(
                    default=None,
                    metadata={
                        "name": "infoCadastro",
                        "type": "Element",
                        "required": True,
                    }
                )
                nova_validade: Optional[TIdePeriodo] = field(
                    default=None,
                    metadata={
                        "name": "novaValidade",
                        "type": "Element",
                    }
                )

            @dataclass
            class Exclusao:
                ide_periodo: Optional[TIdePeriodo] = field(
                    default=None,
                    metadata={
                        "name": "idePeriodo",
                        "type": "Element",
                        "required": True,
                    }
                )
