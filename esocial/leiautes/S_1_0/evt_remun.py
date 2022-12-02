from dataclasses import dataclass, field
from typing import List, Optional
from xsdata.models.datatype import XmlDate

from . import tipos
from .xmldsig_core_schema import Signature

__NAMESPACE__ = "http://www.esocial.gov.br/schema/evt/evtRemun/v_S_01_00_00"


@dataclass
class TInfoAgNocivo:
    class Meta:
        name = "T_infoAgNocivo"

    grau_exp: Optional[str] = field(
        default=None,
        metadata={
            "name": "grauExp",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtRemun/v_S_01_00_00",
            "required": True,
        }
    )


@dataclass
class TItensRemun:
    """
    Itens da remuneração do trabalhador DESCRICAO_COMPLETA:Rubricas que compõem
    a remuneração do trabalhador.

    :ivar cod_rubr: Informar o código atribuído pelo empregador que
        identifica a rubrica em sua folha de pagamento ou o código da
        rubrica constante da Tabela de Rubricas Padrão. Validação: Não
        pode ser utilizada rubrica: a) cujo
        {codIncCP}(1010_infoRubrica_inclusao_dadosRubrica_codIncCP) em
        S-1010 seja igual a [25, 26, 51] se
        {codCateg}(1200_dmDev_codCateg) pertencer ao grupo "Contribuinte
        Individual" ou "Bolsista" da Tabela 01; b) cuja
        {natRubr}(1010_infoRubrica_inclusao_dadosRubrica_natRubr) em
        S-1010 seja igual a [1801, 9220], desde que
        {perApur}(1200_ideEvento_perApur) &gt;= [2021-07] (se
        {indApuracao}(1200_ideEvento_indApuracao) = [1]) ou
        {perApur}(1200_ideEvento_perApur) &gt;= [2021] (se
        {indApuracao}(1200_ideEvento_indApuracao) = [2]).
    :ivar ide_tab_rubr:
    :ivar qtd_rubr:
    :ivar fator_rubr:
    :ivar vr_rubr:
    :ivar ind_apur_ir: Indicativo de tipo de apuração de IR. Validação:
        Informação obrigatória e exclusiva se
        {perApur}(1200_ideEvento_perApur) &gt;= [2021-07] (se
        {indApuracao}(1200_ideEvento_indApuracao) = [1]) ou se
        {perApur}(1200_ideEvento_perApur) &gt;= [2021] (se
        {indApuracao}(1200_ideEvento_indApuracao) = [2]).
    """
    class Meta:
        name = "T_itensRemun"

    cod_rubr: Optional[str] = field(
        default=None,
        metadata={
            "name": "codRubr",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtRemun/v_S_01_00_00",
            "required": True,
        }
    )
    ide_tab_rubr: Optional[str] = field(
        default=None,
        metadata={
            "name": "ideTabRubr",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtRemun/v_S_01_00_00",
            "required": True,
        }
    )
    qtd_rubr: Optional[str] = field(
        default=None,
        metadata={
            "name": "qtdRubr",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtRemun/v_S_01_00_00",
        }
    )
    fator_rubr: Optional[str] = field(
        default=None,
        metadata={
            "name": "fatorRubr",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtRemun/v_S_01_00_00",
        }
    )
    vr_rubr: Optional[str] = field(
        default=None,
        metadata={
            "name": "vrRubr",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtRemun/v_S_01_00_00",
            "required": True,
        }
    )
    ind_apur_ir: Optional[str] = field(
        default=None,
        metadata={
            "name": "indApurIR",
            "type": "Element",
            "namespace": "http://www.esocial.gov.br/schema/evt/evtRemun/v_S_01_00_00",
        }
    )


@dataclass
class Evento:
    """S-1200 - Remuneração de Trabalhador vinculado ao Regime Geral de Previd. Social

    :ivar evt_remun: Evento Remuneração de Trabalhador vinculado ao RGPS
        DESCRICAO_COMPLETA:Evento Remuneração de Trabalhador vinculado
        ao Regime Geral de Previdência Social. CHAVE_GRUPO: {Id}
        REGRA:REGRA_BLOQUEIA_USO_CPF_EMPREGADOR
        REGRA:REGRA_COMPATIBILIDADE_CATEGORIA_CLASSTRIB
        REGRA:REGRA_COMPATIB_REGIME_PREV
        REGRA:REGRA_CONTROLE_DUPLICIDADE REGRA:REGRA_EMPREGADO_DOMESTICO
        REGRA:REGRA_ENVIO_PROC_FECHAMENTO REGRA:REGRA_EVENTOS_EXTEMP
        REGRA:REGRA_EVENTO_POSTERIOR_CAT_OBITO
        REGRA:REGRA_EVE_FOPAG_SIMPLIFICADO
        REGRA:REGRA_EXISTE_INFO_EMPREGADOR
        REGRA:REGRA_GERAL_VALIDA_DADOS_TABCONTRIB
        REGRA:REGRA_MESMO_PROCEMI REGRA:REGRA_REMUN_ANUAL_DEZEMBRO
        REGRA:REGRA_REMUN_CATEG_COMPATIVEL_TPLOTACAO
        REGRA:REGRA_REMUN_CATEG_EXISTENTE_RET
        REGRA:REGRA_REMUN_FGTS_ANTERIOR_ESOCIAL
        REGRA:REGRA_REMUN_IND_RETIFICACAO
        REGRA:REGRA_REMUN_JA_EXISTE_DESLIGAMENTO
        REGRA:REGRA_REMUN_PERMITE_EXCLUSAO
        REGRA:REGRA_REMUN_TRAB_EXISTENTE_RET
        REGRA:REGRA_REMUN_VALIDA_INFO_COMPLEMENTAR
        REGRA:REGRA_RUBRICA_COMPATIVEL_CATEGORIA
        REGRA:REGRA_RUBRICA_COMPATIVEL_DECTERCEIRO
        REGRA:REGRA_RUBRICA_COMPATIVEL_RESC
        REGRA:REGRA_TSV_ATIVO_NA_DTEVENTO REGRA:REGRA_VALIDA_EMPREGADOR
        REGRA:REGRA_VALIDA_PERIODO_APURACAO
    :ivar signature:
    """
    class Meta:
        name = "eSocial"
        namespace = "http://www.esocial.gov.br/schema/evt/evtRemun/v_S_01_00_00"
        schema = "esquemas_xsd_s_1_0/evtRemun.xsd"

    evt_remun: Optional["Evento.EvtRemun"] = field(
        default=None,
        metadata={
            "name": "evtRemun",
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
    class EvtRemun:
        """
        :ivar ide_evento:
        :ivar ide_empregador:
        :ivar ide_trabalhador: Identificação do trabalhador.
            CHAVE_GRUPO: {cpfTrab*}
        :ivar dm_dev: Demonstrativo de valores devidos ao trabalhador
            DESCRICAO_COMPLETA:Identificação de cada um dos
            demonstrativos de valores devidos ao trabalhador.
            CHAVE_GRUPO: {ideDmDev} REGRA:REGRA_DEMONSTRATIVO
        :ivar id:
        """
        ide_evento: Optional[tipos.TIdeEventoFolha] = field(
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
        ide_trabalhador: Optional["Evento.EvtRemun.IdeTrabalhador"] = field(
            default=None,
            metadata={
                "name": "ideTrabalhador",
                "type": "Element",
                "required": True,
            }
        )
        dm_dev: List["Evento.EvtRemun.DmDev"] = field(
            default_factory=list,
            metadata={
                "name": "dmDev",
                "type": "Element",
                "min_occurs": 1,
                "max_occurs": 999,
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
        class IdeTrabalhador:
            """
            :ivar cpf_trab:
            :ivar info_mv: Informação de múltiplos vínculos
                DESCRICAO_COMPLETA:Grupo preenchido exclusivamente em
                caso de trabalhador que possua outros
                vínculos/atividades nos quais já tenha ocorrido desconto
                de contribuição previdenciária. CONDICAO_GRUPO: OC
            :ivar info_complem: Informações complementares de
                identificação do trabalhador DESCRICAO_COMPLETA:Grupo
                preenchido quando o evento de remuneração se referir a
                trabalhador cuja categoria não está sujeita ao evento de
                admissão ou ao evento TSVE - Início, bem como para
                informar remuneração devida pela empresa sucessora a
                empregado desligado ainda na sucedida. No caso das
                categorias em que o envio do evento TSVE - Início for
                opcional, o preenchimento do grupo somente é exigido se
                não houver o respectivo evento. As informações
                complementares são necessárias para correta
                identificação do trabalhador. CONDICAO_GRUPO: O ((se o
                trabalhador não tiver nenhum cadastro no RET) OU (se
                {remunSuc}(1200_dmDev_infoPerAnt_ideADC_remunSuc) =
                [S])); N (se o trabalhador tiver cadastro ativo no RET);
                OC (nos demais casos)
            :ivar proc_jud_trab:
            :ivar info_interm: Informações relativas ao trabalho
                intermitente. CHAVE_GRUPO: {dia} CONDICAO_GRUPO: O (se
                {codCateg}(1200_dmDev_codCateg) = [111] em
                {perApur}(1200_ideEvento_perApur),
                {indApuracao}(1200_ideEvento_indApuracao) = [1] e
                existir o grupo {infoPerApur}(1200_dmDev_infoPerApur));
                N (nos demais casos)
            """
            cpf_trab: Optional[str] = field(
                default=None,
                metadata={
                    "name": "cpfTrab",
                    "type": "Element",
                    "required": True,
                }
            )
            info_mv: Optional["Evento.EvtRemun.IdeTrabalhador.InfoMv"] = field(
                default=None,
                metadata={
                    "name": "infoMV",
                    "type": "Element",
                }
            )
            info_complem: Optional["Evento.EvtRemun.IdeTrabalhador.InfoComplem"] = field(
                default=None,
                metadata={
                    "name": "infoComplem",
                    "type": "Element",
                }
            )
            proc_jud_trab: List[str] = field(
                default_factory=list,
                metadata={
                    "name": "procJudTrab",
                    "type": "Element",
                    "max_occurs": 99,
                }
            )
            info_interm: List[str] = field(
                default_factory=list,
                metadata={
                    "name": "infoInterm",
                    "type": "Element",
                    "max_occurs": 31,
                }
            )

            @dataclass
            class InfoMv:
                """
                :ivar ind_mv:
                :ivar remun_outr_empr: Remuneração recebida pelo
                    trabalhador em outras empresas ou atividades
                    DESCRICAO_COMPLETA:Informações relativas ao
                    trabalhador que possui vínculo empregatício com
                    outra(s) empresa(s) e/ou que exerce outras
                    atividades como contribuinte individual, detalhando
                    as empresas que efetuaram (ou efetuarão) desconto da
                    contribuição. CHAVE_GRUPO: {tpInsc}, {nrInsc},
                    {codCateg}
                """
                ind_mv: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "indMV",
                        "type": "Element",
                        "required": True,
                    }
                )
                remun_outr_empr: List["Evento.EvtRemun.IdeTrabalhador.InfoMv.RemunOutrEmpr"] = field(
                    default_factory=list,
                    metadata={
                        "name": "remunOutrEmpr",
                        "type": "Element",
                        "min_occurs": 1,
                        "max_occurs": 999,
                    }
                )

                @dataclass
                class RemunOutrEmpr:
                    """
                    :ivar tp_insc:
                    :ivar nr_insc: Informar o número de inscrição do
                        contribuinte de acordo com o tipo de inscrição
                        indicado no campo
                        {remunOutrEmpr/tpInsc}(./tpInsc). Validação: a)
                        Se {indApuracao}(1200_ideEvento_indApuracao) =
                        [1] e {remunOutrEmpr/tpInsc}(./tpInsc) = [1],
                        deve ser um CNPJ válido, diferente do CNPJ base
                        indicado no evento de Informações do Empregador
                        (S-1000) e dos estabelecimentos informados
                        através do evento S-1005. b) Se
                        {indApuracao}(1200_ideEvento_indApuracao) = [1]
                        e {remunOutrEmpr/tpInsc}(./tpInsc) = [2], deve
                        ser um CPF válido e diferente do CPF do
                        trabalhador e ainda, caso o empregador seja
                        pessoa física, diferente do CPF do empregador.
                        c) Se {indApuracao}(1200_ideEvento_indApuracao)
                        = [2] e {remunOutrEmpr/tpInsc}(./tpInsc) = [1],
                        é permitido informar número de inscrição igual
                        ao CNPJ base indicado no evento de Informações
                        do Empregador (S-1000) e aos estabelecimentos
                        informados através do evento S-1005. d) Se
                        {indApuracao}(1200_ideEvento_indApuracao) = [2]
                        e {remunOutrEmpr/tpInsc}(./tpInsc) = [2], deve
                        ser um CPF válido e diferente do CPF do
                        trabalhador, mas é permitido informar número de
                        inscrição igual ao CPF do empregador.
                    :ivar cod_categ:
                    :ivar vlr_remun_oe:
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
                    cod_categ: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "codCateg",
                            "type": "Element",
                            "required": True,
                        }
                    )
                    vlr_remun_oe: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "vlrRemunOE",
                            "type": "Element",
                            "required": True,
                        }
                    )

            @dataclass
            class InfoComplem:
                """
                :ivar nm_trab:
                :ivar dt_nascto:
                :ivar sucessao_vinc: Grupo de informações da sucessão de
                    vínculo trabalhista. CONDICAO_GRUPO: O (se
                    {remunSuc}(1200_dmDev_infoPerAnt_ideADC_remunSuc) =
                    [S]); N (nos demais casos)
                """
                nm_trab: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "nmTrab",
                        "type": "Element",
                        "required": True,
                    }
                )
                dt_nascto: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "dtNascto",
                        "type": "Element",
                        "required": True,
                    }
                )
                sucessao_vinc: Optional["Evento.EvtRemun.IdeTrabalhador.InfoComplem.SucessaoVinc"] = field(
                    default=None,
                    metadata={
                        "name": "sucessaoVinc",
                        "type": "Element",
                    }
                )

                @dataclass
                class SucessaoVinc:
                    """
                    :ivar tp_insc:
                    :ivar nr_insc: Informar o número de inscrição do
                        empregador anterior, de acordo com o tipo de
                        inscrição indicado no campo
                        {sucessaoVinc/tpInsc}(./tpInsc). Validação: Deve
                        ser um número de inscrição válido e diferente da
                        inscrição do declarante, considerando as
                        particularidades aplicadas à informação de CNPJ
                        de órgão público em S-1000. Se
                        {sucessaoVinc/tpInsc}(./tpInsc) = [1], deve
                        possuir 14 (catorze) algarismos e ser diferente
                        do CNPJ base do empregador (exceto se
                        {ideEmpregador/nrInsc}(1200_ideEmpregador_nrInsc)
                        tiver 14 (catorze) algarismos) e dos
                        estabelecimentos informados através do evento
                        S-1005. Se {sucessaoVinc/tpInsc}(./tpInsc) =
                        [2], deve possuir 11 (onze) algarismos.
                    :ivar matric_ant:
                    :ivar dt_adm:
                    :ivar observacao:
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
                    matric_ant: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "matricAnt",
                            "type": "Element",
                        }
                    )
                    dt_adm: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "dtAdm",
                            "type": "Element",
                            "required": True,
                        }
                    )
                    observacao: Optional[str] = field(
                        default=None,
                        metadata={
                            "type": "Element",
                        }
                    )

        @dataclass
        class DmDev:
            """
            :ivar ide_dm_dev: Identificador atribuído pela empresa para
                o demonstrativo de valores devidos ao trabalhador. O
                empregador pode preencher este campo utilizando-se de um
                identificador padrão para todos os trabalhadores; no
                entanto, havendo mais de um demonstrativo relativo a uma
                mesma competência, devem ser utilizados identificadores
                diferentes para cada um dos demonstrativos. Validação:
                Deve ser um identificador único dentro do mesmo
                {perApur}(1200_ideEvento_perApur) para cada um dos
                demonstrativos do trabalhador.
                REGRA:REGRA_CARACTERE_ESPECIAL
            :ivar cod_categ:
            :ivar info_per_apur: Informações relativas ao período de
                apuração. CONDICAO_GRUPO: O (se não existir o grupo
                {infoPerAnt}(1200_dmDev_infoPerAnt)); OC (nos demais
                casos)
            :ivar info_per_ant: Informações relativas a períodos
                anteriores DESCRICAO_COMPLETA:Grupo destinado às
                informações de: a) remuneração relativa a diferenças
                salariais provenientes de acordo coletivo, convenção
                coletiva e dissídio; b) remuneração relativa a
                diferenças de vencimento provenientes de disposições
                legais; c) bases de cálculo para efeitos de apuração de
                FGTS resultantes de conversão de licença saúde em
                acidente de trabalho; d) verbas de natureza salarial ou
                não salarial devidas após o desligamento. OBS.: As
                informações previstas acima podem se referir ao período
                de apuração definido em
                {perApur}(1200_ideEvento_perApur) ou a períodos
                anteriores a {perApur}(1200_ideEvento_perApur).
                CONDICAO_GRUPO: N (se
                {indApuracao}(1200_ideEvento_indApuracao) = [2] ou
                {codCateg}(1200_dmDev_codCateg) for diferente de [1XX,
                2XX, 3XX, 4XX, 721, 722, 901]); O (se não existir o
                grupo {infoPerApur}(1200_dmDev_infoPerApur) e
                {indApuracao}(1200_ideEvento_indApuracao) = [1]); OC
                (nos demais casos)
            :ivar info_compl_cont: Informações complementares
                contratuais do trabalhador DESCRICAO_COMPLETA:Grupo
                preenchido exclusivamente quando o evento de remuneração
                se referir a trabalhador cuja categoria não estiver
                obrigada ao evento de início de TSVE e se não houver
                evento S-2300 correspondente. CONDICAO_GRUPO: O ((se
                {codCateg}(1200_dmDev_codCateg) = [2XX, 304, 305, 4XX,
                5XX, 7XX, 902]) E (se para o trabalhador não houver
                evento S-2300 ativo) E (se não for informado
                {remunPerApur/matricula}(1200_dmDev_infoPerApur_ideEstabLot_remunPerApur_matricula)
                ou
                {remunPerAnt/matricula}(1200_dmDev_infoPerAnt_ideADC_idePeriodo_ideEstabLot_remunPerAnt_matricula)));
                OC ((se {codCateg}(1200_dmDev_codCateg) = [901, 903,
                904]) E (se para o trabalhador não houver evento S-2300
                ativo) E (se não for informado
                {remunPerApur/matricula}(1200_dmDev_infoPerApur_ideEstabLot_remunPerApur_matricula)
                ou
                {remunPerAnt/matricula}(1200_dmDev_infoPerAnt_ideADC_idePeriodo_ideEstabLot_remunPerAnt_matricula)));
                N (nos demais casos)
            """
            ide_dm_dev: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ideDmDev",
                    "type": "Element",
                    "required": True,
                }
            )
            cod_categ: Optional[str] = field(
                default=None,
                metadata={
                    "name": "codCateg",
                    "type": "Element",
                    "required": True,
                }
            )
            info_per_apur: Optional["Evento.EvtRemun.DmDev.InfoPerApur"] = field(
                default=None,
                metadata={
                    "name": "infoPerApur",
                    "type": "Element",
                }
            )
            info_per_ant: Optional["Evento.EvtRemun.DmDev.InfoPerAnt"] = field(
                default=None,
                metadata={
                    "name": "infoPerAnt",
                    "type": "Element",
                }
            )
            info_compl_cont: Optional["Evento.EvtRemun.DmDev.InfoComplCont"] = field(
                default=None,
                metadata={
                    "name": "infoComplCont",
                    "type": "Element",
                }
            )

            @dataclass
            class InfoPerApur:
                """
                :ivar ide_estab_lot: Identificação do estabelecimento e
                    lotação DESCRICAO_COMPLETA:Identificação do
                    estabelecimento e da lotação nos quais o trabalhador
                    possui remuneração no período de apuração. O
                    estabelecimento identificado no grupo pode ser: o
                    número do CNPJ do estabelecimento da própria empresa
                    (matriz/filial), o número da obra (própria) no CNO,
                    ou o número do CAEPF (no caso de pessoa física
                    obrigada a inscrição no Cadastro de Atividade
                    Econômica da Pessoa Física). CHAVE_GRUPO: {tpInsc},
                    {nrInsc}, {codLotacao}
                """
                ide_estab_lot: List["Evento.EvtRemun.DmDev.InfoPerApur.IdeEstabLot"] = field(
                    default_factory=list,
                    metadata={
                        "name": "ideEstabLot",
                        "type": "Element",
                        "min_occurs": 1,
                        "max_occurs": 500,
                    }
                )

                @dataclass
                class IdeEstabLot:
                    """
                    :ivar tp_insc:
                    :ivar nr_insc:
                    :ivar cod_lotacao:
                    :ivar qtd_dias_av: Quantidade de dias trabalhados no
                        mês pelo trabalhador avulso no tomador de
                        serviços identificado em
                        {ideEstabLot/codLotacao}(1200_dmDev_infoPerApur_ideEstabLot_codLotacao).
                        Cada dia, total ou parcial, em que o trabalhador
                        tenha prestado serviços ao tomador deve ser
                        considerado. Ex.: Se, em um mesmo mês, o
                        trabalhador prestou serviços durante uma hora em
                        um dia e durante mais uma hora em outro dia,
                        deve-se informar a quantidade de 2 dias. Caso
                        não tenha havido trabalho no mês, informar 0
                        (zero). Validação: Informação obrigatória e
                        exclusiva se
                        {ideEstabLot/codLotacao}(./codLotacao) possuir
                        {tpLotacao}(1020_infoLotacao_inclusao_dadosLotacao_tpLotacao)
                        em S-1020 = [08, 09] em
                        {perApur}(1200_ideEvento_perApur) e se
                        {indApuracao}(1200_ideEvento_indApuracao) = [1].
                        Se informado, deve ser um número entre 0 e 31,
                        de acordo com o calendário anual.
                    :ivar remun_per_apur: Remuneração do trabalhador
                        DESCRICAO_COMPLETA:Informações relativas à
                        remuneração do trabalhador no período de
                        apuração. CHAVE_GRUPO: {matricula}
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
                    cod_lotacao: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "codLotacao",
                            "type": "Element",
                            "required": True,
                        }
                    )
                    qtd_dias_av: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "qtdDiasAv",
                            "type": "Element",
                        }
                    )
                    remun_per_apur: List["Evento.EvtRemun.DmDev.InfoPerApur.IdeEstabLot.RemunPerApur"] = field(
                        default_factory=list,
                        metadata={
                            "name": "remunPerApur",
                            "type": "Element",
                            "min_occurs": 1,
                            "max_occurs": 8,
                        }
                    )

                    @dataclass
                    class RemunPerApur:
                        """
                        :ivar matricula: Matrícula atribuída ao
                            trabalhador pela empresa ou, no caso de
                            servidor público, a matrícula constante no
                            Sistema de Administração de Recursos Humanos
                            do órgão. Validação: Deve corresponder à
                            matrícula informada pelo empregador no
                            evento S-2190, S-2200 ou S-2300 do
                            respectivo contrato. Não preencher no caso
                            de Trabalhador Sem Vínculo de
                            Emprego/Estatutário - TSVE sem informação de
                            matrícula no evento S-2300.
                        :ivar ind_simples:
                        :ivar itens_remun:
                        :ivar info_ag_nocivo: Grau de exposição a
                            agentes nocivos DESCRICAO_COMPLETA:Grupo
                            referente ao detalhamento do grau de
                            exposição do trabalhador aos agentes nocivos
                            que ensejam a cobrança da contribuição
                            adicional para financiamento dos benefícios
                            de aposentadoria especial. CONDICAO_GRUPO: O
                            (se {codCateg}(1200_dmDev_codCateg) = [1XX,
                            2XX, 3XX, 731, 734, 738] ou se
                            {codCateg}(1200_dmDev_codCateg) = [4XX] com
                            {categOrig} em S-2300 = [1XX, 2XX, 3XX, 731,
                            734, 738]); N (nos demais casos)
                        """
                        matricula: Optional[str] = field(
                            default=None,
                            metadata={
                                "type": "Element",
                            }
                        )
                        ind_simples: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "indSimples",
                                "type": "Element",
                            }
                        )
                        itens_remun: List[TItensRemun] = field(
                            default_factory=list,
                            metadata={
                                "name": "itensRemun",
                                "type": "Element",
                                "min_occurs": 1,
                                "max_occurs": 200,
                            }
                        )
                        info_ag_nocivo: Optional[TInfoAgNocivo] = field(
                            default=None,
                            metadata={
                                "name": "infoAgNocivo",
                                "type": "Element",
                            }
                        )

            @dataclass
            class InfoPerAnt:
                """
                :ivar ide_adc: Instrumento ou situação ensejadora da
                    remuneração em períodos anteriores
                    DESCRICAO_COMPLETA:Identificação do instrumento ou
                    situação ensejadora da remuneração relativa a
                    períodos de apuração anteriores. CHAVE_GRUPO:
                    {dtAcConv}, {tpAcConv}
                """
                ide_adc: List["Evento.EvtRemun.DmDev.InfoPerAnt.IdeAdc"] = field(
                    default_factory=list,
                    metadata={
                        "name": "ideADC",
                        "type": "Element",
                        "min_occurs": 1,
                        "max_occurs": 8,
                    }
                )

                @dataclass
                class IdeAdc:
                    """
                    :ivar dt_ac_conv:
                    :ivar tp_ac_conv: Tipo do instrumento ou situação
                        ensejadora da remuneração relativa a períodos de
                        apuração anteriores. Validação: Se
                        {classTrib}(1000_infoEmpregador_inclusao_infoCadastro_classTrib)
                        em S-1000 = [04, 22], não pode ser informado [E,
                        H].
                    :ivar dsc:
                    :ivar remun_suc: Indicar se a remuneração é relativa
                        a verbas de natureza salarial ou não salarial
                        devidas pela empresa sucessora a empregados
                        desligados ainda na sucedida.
                    :ivar ide_periodo: Identificação do período de
                        referência da remuneração
                        DESCRICAO_COMPLETA:Identificação do período ao
                        qual se referem as diferenças de remuneração.
                        CHAVE_GRUPO: {perRef}
                    """
                    dt_ac_conv: Optional[XmlDate] = field(
                        default=None,
                        metadata={
                            "name": "dtAcConv",
                            "type": "Element",
                            "min_inclusive": XmlDate(1890, 1, 1),
                        }
                    )
                    tp_ac_conv: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "tpAcConv",
                            "type": "Element",
                            "required": True,
                        }
                    )
                    dsc: Optional[str] = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "required": True,
                        }
                    )
                    remun_suc: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "remunSuc",
                            "type": "Element",
                            "required": True,
                        }
                    )
                    ide_periodo: List["Evento.EvtRemun.DmDev.InfoPerAnt.IdeAdc.IdePeriodo"] = field(
                        default_factory=list,
                        metadata={
                            "name": "idePeriodo",
                            "type": "Element",
                            "min_occurs": 1,
                            "max_occurs": 180,
                        }
                    )

                    @dataclass
                    class IdePeriodo:
                        """
                        :ivar per_ref: Informar o período ao qual se
                            refere o complemento de remuneração, no
                            formato AAAA-MM. Validação: Deve ser igual
                            ou anterior ao período de apuração informado
                            em {perApur}(/ideEvento_perApur). Deve ser
                            informado no formato AAAA-MM. Se
                            {tpAcConv}(../tpAcConv) = [H], deve ser
                            anterior ao início dos eventos periódicos
                            para o empregador no eSocial.
                        :ivar ide_estab_lot: Identificação do
                            estabelecimento e lotação
                            DESCRICAO_COMPLETA:Identificação do
                            estabelecimento e da lotação ao qual se
                            referem as diferenças de remuneração do mês
                            identificado no grupo superior. CHAVE_GRUPO:
                            {tpInsc}, {nrInsc}, {codLotacao}
                        """
                        per_ref: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "perRef",
                                "type": "Element",
                                "required": True,
                            }
                        )
                        ide_estab_lot: List["Evento.EvtRemun.DmDev.InfoPerAnt.IdeAdc.IdePeriodo.IdeEstabLot"] = field(
                            default_factory=list,
                            metadata={
                                "name": "ideEstabLot",
                                "type": "Element",
                                "min_occurs": 1,
                                "max_occurs": 500,
                            }
                        )

                        @dataclass
                        class IdeEstabLot:
                            """
                            :ivar tp_insc:
                            :ivar nr_insc:
                            :ivar cod_lotacao:
                            :ivar remun_per_ant: Remuneração do
                                trabalhador
                                DESCRICAO_COMPLETA:Informações relativas
                                à remuneração do trabalhador em períodos
                                anteriores. CHAVE_GRUPO: {matricula}
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
                            cod_lotacao: Optional[str] = field(
                                default=None,
                                metadata={
                                    "name": "codLotacao",
                                    "type": "Element",
                                    "required": True,
                                }
                            )
                            remun_per_ant: List["Evento.EvtRemun.DmDev.InfoPerAnt.IdeAdc.IdePeriodo.IdeEstabLot.RemunPerAnt"] = field(
                                default_factory=list,
                                metadata={
                                    "name": "remunPerAnt",
                                    "type": "Element",
                                    "min_occurs": 1,
                                    "max_occurs": 8,
                                }
                            )

                            @dataclass
                            class RemunPerAnt:
                                """
                                :ivar matricula: Matrícula atribuída ao
                                    trabalhador pela empresa ou, no caso
                                    de servidor público, a matrícula
                                    constante no Sistema de
                                    Administração de Recursos Humanos do
                                    órgão. Validação: Deve corresponder
                                    à matrícula informada pelo
                                    empregador no evento S-2190, S-2200
                                    ou S-2300 do respectivo contrato.
                                    Não preencher no caso de TSVE sem
                                    informação de matrícula no evento
                                    S-2300 ou se
                                    {remunSuc}(1200_dmDev_infoPerAnt_ideADC_remunSuc)
                                    = [S].
                                :ivar ind_simples:
                                :ivar itens_remun:
                                :ivar info_ag_nocivo: Grau de exposição
                                    a agentes nocivos
                                    DESCRICAO_COMPLETA:Grupo referente
                                    ao detalhamento do grau de exposição
                                    do trabalhador aos agentes nocivos
                                    que ensejam a cobrança da
                                    contribuição adicional para
                                    financiamento dos benefícios de
                                    aposentadoria especial.
                                    CONDICAO_GRUPO: O (se
                                    {codCateg}(1200_dmDev_codCateg) =
                                    [1XX, 2XX, 3XX] ou se
                                    {codCateg}(1200_dmDev_codCateg) =
                                    [4XX] com {categOrig} em S-2300 =
                                    [1XX, 2XX, 3XX]); N (nos demais
                                    casos)
                                """
                                matricula: Optional[str] = field(
                                    default=None,
                                    metadata={
                                        "type": "Element",
                                    }
                                )
                                ind_simples: Optional[str] = field(
                                    default=None,
                                    metadata={
                                        "name": "indSimples",
                                        "type": "Element",
                                    }
                                )
                                itens_remun: List[TItensRemun] = field(
                                    default_factory=list,
                                    metadata={
                                        "name": "itensRemun",
                                        "type": "Element",
                                        "min_occurs": 1,
                                        "max_occurs": 200,
                                    }
                                )
                                info_ag_nocivo: Optional[TInfoAgNocivo] = field(
                                    default=None,
                                    metadata={
                                        "name": "infoAgNocivo",
                                        "type": "Element",
                                    }
                                )

            @dataclass
            class InfoComplCont:
                """
                :ivar cod_cbo: Classificação Brasileira de Ocupações -
                    CBO. Validação: Deve ser um código válido e
                    existente na tabela de CBO, com 6 (seis) posições.
                :ivar nat_atividade: Natureza da atividade. Validação: O
                    campo deve ser preenchido apenas se atendida uma das
                    condições a seguir apresentadas: a)
                    {classTrib}(1000_infoEmpregador_inclusao_infoCadastro_classTrib)
                    em S-1000 = [06, 07]; b)
                    {classTrib}(1000_infoEmpregador_inclusao_infoCadastro_classTrib)
                    em S-1000 = [21, 22] e existir remuneração para o
                    trabalhador vinculada a um tipo de CAEPF informado
                    em S-1005 como produtor rural ou segurado especial.
                :ivar qtd_dias_trab: Informação prestada exclusivamente
                    pelo segurado especial em caso de contratação de
                    contribuinte individual, indicando a quantidade de
                    dias trabalhados pelo mesmo. Caso não tenha havido
                    trabalho no mês, informar 0 (zero). Validação:
                    Preenchimento obrigatório e exclusivo se
                    {classTrib}(1000_infoEmpregador_inclusao_infoCadastro_classTrib)
                    em S-1000 = [22], {natAtividade}(./natAtividade) =
                    [2] e {indApuracao}(1200_ideEvento_indApuracao) =
                    [1]. Neste caso, preencher com um número entre 0 e
                    31, de acordo com o calendário anual.
                """
                cod_cbo: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "codCBO",
                        "type": "Element",
                        "required": True,
                    }
                )
                nat_atividade: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "natAtividade",
                        "type": "Element",
                    }
                )
                qtd_dias_trab: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "qtdDiasTrab",
                        "type": "Element",
                    }
                )
