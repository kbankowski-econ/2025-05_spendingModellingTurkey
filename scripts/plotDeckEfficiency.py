"""
Türkiye deck, spending-efficiency slide: the additional output gain over time
from gradually closing spending-efficiency gaps, over and above the
reallocation-only baseline, for advanced economies, EMDEs and Türkiye.

Each line is the efficiency-closing scenario minus its own reallocation
baseline. Every panel closes its gap by 2050. EMDEs and Türkiye are also run at
a faster speed, closing by 2040, but the advanced-economy set is not, and the
slide shows the one closure horizon all three calibrations have in common.
"""
from deck_lines import (
    INFRA, HUMAN_CAPITAL, RD, LABEL_BG_SENSITIVITY, Panel, Series, Slide, render_slide,
)

INFRA_LABEL = "Infrastructure"
HC_LABEL = "Human capital"
RD_LABEL = "R&D"

SLIDE = Slide(
    panels=[
        Panel("efficiencyAE_yd_lines", [
            Series(INFRA_LABEL, "Model_HumanCapital_epsi_igeff25y___yd",
                   INFRA, base="Model_HumanCapital_epsi_ig___yd"),
            Series(HC_LABEL, "Model_HumanCapital_epsi_cgeeff25y___yd",
                   HUMAN_CAPITAL, base="Model_HumanCapital_epsi_cge___yd"),
            Series(RD_LABEL, "Model_HumanCapital_epsi_cgrd_eff25y___yd",
                   RD, base="Model_HumanCapital_epsi_cgrd___yd"),
        ], color_legend=[(INFRA_LABEL, INFRA), (HC_LABEL, HUMAN_CAPITAL), (RD_LABEL, RD)]),
        Panel("efficiencyEM_yd_lines", [
            Series(INFRA_LABEL, "EM_Model_HumanCapital_epsiigeff25y___yd",
                   INFRA, base="EM_Model_HumanCapital_epsiig___yd"),
            Series(HC_LABEL, "EM_Model_HumanCapital_epsicgeeff25y___yd",
                   HUMAN_CAPITAL, base="EM_Model_HumanCapital_epsicge___yd"),
        ]),
        Panel("efficiencyTR_yd_lines", [
            Series(INFRA_LABEL, "TR_Model_HumanCapital_epsiigeff25y___yd",
                   INFRA, base="TR_Model_HumanCapital_epsiig___yd"),
            Series(HC_LABEL, "TR_Model_HumanCapital_epsicgeeff25y___yd",
                   HUMAN_CAPITAL, base="TR_Model_HumanCapital_epsicge___yd"),
        ]),
        # Sensitivity: Türkiye on the Fiscal Monitor gaps. Rendered here rather
        # than on its own so it shares the y-range with the main panels.
        Panel("efficiencyTRfm_yd_lines", [
            Series(INFRA_LABEL, "TR_Model_HumanCapital_epsiigeff25yfm___yd",
                   INFRA, base="TR_Model_HumanCapital_epsiigfm___yd"),
            Series(HC_LABEL, "TR_Model_HumanCapital_epsicgeeff25yfm___yd",
                   HUMAN_CAPITAL, base="TR_Model_HumanCapital_epsicgefm___yd"),
        ], label_bgcolor=LABEL_BG_SENSITIVITY),
    ],
    color_legend=[(INFRA_LABEL, INFRA), (HC_LABEL, HUMAN_CAPITAL)],
)


if __name__ == "__main__":
    render_slide(SLIDE)
