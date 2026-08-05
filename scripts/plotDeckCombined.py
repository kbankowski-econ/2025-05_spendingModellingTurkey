"""
Türkiye deck, combined slide: output gains from a reallocation of expenditure
together with a gradual closure of the corresponding spending-efficiency gap,
for advanced economies, EMDEs and Türkiye.

The closure horizon is 2050 in all three panels. EMDEs and Türkiye also have a
2040 closure, but the advanced-economy set does not, and a slide whose three
panels close their gaps on different dates cannot be read across. The
reallocation-only paths these lines build on are the deck's reallocation slide.
"""
from deck_lines import (
    INFRA, HUMAN_CAPITAL, RD, LABEL_BG_SENSITIVITY, Panel, Series, Slide, render_slide,
)

INFRA_LABEL = "Infrastructure"
HC_LABEL = "Human capital"
RD_LABEL = "R&D"

SLIDE = Slide(
    panels=[
        # Only the advanced-economy set has an R&D experiment, and only there
        # does the R&D efficiency gap feed technology creation.
        Panel("combinedAE_yd_lines", [
            Series(INFRA_LABEL, "Model_HumanCapital_epsi_igeff25y___yd", INFRA),
            Series(HC_LABEL, "Model_HumanCapital_epsi_cgeeff25y___yd", HUMAN_CAPITAL),
            Series(RD_LABEL, "Model_HumanCapital_epsi_cgrd_eff25y___yd", RD),
        ], color_legend=[(INFRA_LABEL, INFRA), (HC_LABEL, HUMAN_CAPITAL), (RD_LABEL, RD)]),
        Panel("combinedEM_yd_lines", [
            Series(INFRA_LABEL, "EM_Model_HumanCapital_epsiigeff25y___yd", INFRA),
            Series(HC_LABEL, "EM_Model_HumanCapital_epsicgeeff25y___yd", HUMAN_CAPITAL),
        ]),
        Panel("combinedTR_yd_lines", [
            Series(INFRA_LABEL, "TR_Model_HumanCapital_epsiigeff25y___yd", INFRA),
            Series(HC_LABEL, "TR_Model_HumanCapital_epsicgeeff25y___yd", HUMAN_CAPITAL),
        ]),
        # Sensitivity: Türkiye on the Fiscal Monitor gaps. Rendered here rather
        # than on its own so it shares the y-range with the main panels.
        Panel("combinedTRfm_yd_lines", [
            Series(INFRA_LABEL, "TR_Model_HumanCapital_epsiigeff25yfm___yd", INFRA),
            Series(HC_LABEL, "TR_Model_HumanCapital_epsicgeeff25yfm___yd", HUMAN_CAPITAL),
        ], label_bgcolor=LABEL_BG_SENSITIVITY),
    ],
    color_legend=[(INFRA_LABEL, INFRA), (HC_LABEL, HUMAN_CAPITAL)],
)


if __name__ == "__main__":
    render_slide(SLIDE)
