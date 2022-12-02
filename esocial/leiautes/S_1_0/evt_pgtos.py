from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate

from . import tipos
from .xmldsig_core_schema import Signature

__NAMESPACE__ = "http://www.esocial.gov.br/schema/evt/evtPgtos/v_S_01_00_00"


class InfoPgtoTpPgto(Enum):
    """
    Informar o evento de origem do pagamento.

    :cvar VALUE_1: Pagamento de remuneração, conforme apurado em
        {ideDmDev}(1200_dmDev_ideDmDev) do S-1200
    :cvar VALUE_2: Pagamento de verbas rescisórias conforme apurado em
        {ideDmDev}(2299_infoDeslig_verbasResc_dmDev_ideDmDev) do S-2299
    :cvar VALUE_3: Pagamento de verbas rescisórias conforme apurado em
        {ideDmDev}(2399_infoTSVTermino_verbasResc_dmDev_ideDmDev) do
        S-2399
    :cvar VALUE_4: Pagamento de remuneração conforme apurado em
        {ideDmDev}(1202_dmDev_ideDmDev) do S-1202
    :cvar VALUE_5: Pagamento de benefícios previdenciários, conforme
        apurado em {ideDmDev}(1207_dmDev_ideDmDev) do S-1207
    """
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5


@dataclass
class Evento:
    """S-1210 - Pagamentos de Rendimentos do Trabalho

    :ivar evt_pgtos: Evento Pagamentos de Rendimentos do Trabalho.
        CHAVE_GRUPO: {Id} REGRA:REGRA_CONTROLE_DUPLICIDADE
        REGRA:REGRA_EMPREGADO_DOMESTICO
        REGRA:REGRA_ENVIO_PROC_FECHAMENTO REGRA:REGRA_EVENTOS_EXTEMP
        REGRA:REGRA_EVE_FOPAG_SIMPLIFICADO
        REGRA:REGRA_EXISTE_INFO_EMPREGADOR REGRA:REGRA_MESMO_PROCEMI
        REGRA:REGRA_PAGTO_IND_RETIFICACAO REGRA:REGRA_VALIDA_DT_PGTO
        REGRA:REGRA_VALIDA_EMPREGADOR REGRA:REGRA_VALIDA_PER_APUR_PGTO
    :ivar signature:
    """
    class Meta:
        name = "eSocial"
        namespace = "http://www.esocial.gov.br/schema/evt/evtPgtos/v_S_01_00_00"
        schema = "esquemas_xsd_s_1_0/evtPgtos.xsd"

    evt_pgtos: Optional["Evento.EvtPgtos"] = field(
        default=None,
        metadata={
            "name": "evtPgtos",
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
    class EvtPgtos:
        """
        :ivar ide_evento:
        :ivar ide_empregador:
        :ivar ide_benef: Identificação do beneficiário do pagamento.
            CHAVE_GRUPO: {cpfBenef*}
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
        ide_benef: Optional["Evento.EvtPgtos.IdeBenef"] = field(
            default=None,
            metadata={
                "name": "ideBenef",
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
        class IdeBenef:
            """
            :ivar cpf_benef: Informar o CPF do beneficiário. Validação:
                Deve ser o mesmo CPF informado no evento de remuneração
                ou desligamento (S-1200, S-1202, S-1207, S-2299 ou
                S-2399).
            :ivar info_pgto: Informações dos pagamentos efetuados.
                CHAVE_GRUPO: {tpPgto}, {perRef}, {ideDmDev}
            """
            cpf_benef: Optional[str] = field(
                default=None,
                metadata={
                    "name": "cpfBenef",
                    "type": "Element",
                    "required": True,
                }
            )
            info_pgto: List["Evento.EvtPgtos.IdeBenef.InfoPgto"] = field(
                default_factory=list,
                metadata={
                    "name": "infoPgto",
                    "type": "Element",
                    "min_occurs": 1,
                    "max_occurs": 999,
                }
            )

            @dataclass
            class InfoPgto:
                """
                :ivar dt_pgto: Informar a data de pagamento. Validação:
                    A data informada deve estar compreendida no período
                    de apuração ({perApur}(1210_ideEvento_perApur)),
                    exceto se {procEmi}(1210_ideEvento_procEmi) = [2, 4,
                    22].
                :ivar tp_pgto:
                :ivar per_ref: Informar a competência declarada no campo
                    {perApur} do evento remuneratório a que se refere o
                    pagamento, no formato AAAA-MM (ou AAAA, se for
                    relativa à folha de 13° salário). Se
                    {tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [2, 3],
                    informar o mês/ano da data de desligamento (ou de
                    término), no formato AAAA-MM. Validação: Deve
                    corresponder ao conteúdo indicado na relação a
                    seguir: Se {tpPgto}(1210_ideBenef_infoPgto_tpPgto) =
                    [1], {perApur}(1200_ideEvento_perApur) do S-1200; Se
                    {tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [2],
                    mês/ano de {dtDeslig}(2299_infoDeslig_dtDeslig) do
                    S-2299 (formato AAAA-MM); Se
                    {tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [3],
                    mês/ano de {dtTerm}(2399_infoTSVTermino_dtTerm) do
                    S-2399 (formato AAAA-MM); Se
                    {tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [4],
                    {perApur}(1202_ideEvento_perApur) do S-1202; Se
                    {tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [5],
                    {perApur}(1207_ideEvento_perApur) do S-1207.
                :ivar ide_dm_dev: Identificador atribuído pela fonte
                    pagadora para o demonstrativo de valores devidos ao
                    trabalhador conforme definido em S-1200, S-1202,
                    S-1207, S-2299 ou S-2399. Validação: Deve ser um
                    valor atribuído pela fonte pagadora em S-1200,
                    S-1202, S-1207, S-2299 ou S-2399 no campo
                    {ideDmDev}, obedecendo à relação: Se
                    {tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [1], em
                    S-1200; Se {tpPgto}(1210_ideBenef_infoPgto_tpPgto) =
                    [2], em S-2299; Se
                    {tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [3], em
                    S-2399; Se {tpPgto}(1210_ideBenef_infoPgto_tpPgto) =
                    [4], em S-1202; Se
                    {tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [5], em
                    S-1207.
                :ivar vr_liq: Valor líquido recebido pelo trabalhador,
                    composto pelos vencimentos e descontos, inclusive os
                    descontos de IRRF e de pensão alimentícia (se
                    houver). Validação: Não pode ser um valor negativo.
                """
                dt_pgto: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "dtPgto",
                        "type": "Element",
                        "required": True,
                    }
                )
                tp_pgto: Optional[InfoPgtoTpPgto] = field(
                    default=None,
                    metadata={
                        "name": "tpPgto",
                        "type": "Element",
                        "required": True,
                    }
                )
                per_ref: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "perRef",
                        "type": "Element",
                        "required": True,
                    }
                )
                ide_dm_dev: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "ideDmDev",
                        "type": "Element",
                        "required": True,
                    }
                )
                vr_liq: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "vrLiq",
                        "type": "Element",
                        "required": True,
                    }
                )
