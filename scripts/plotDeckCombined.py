"""
Türkiye deck, combined slide: output gains from a reallocation of expenditure
together with a gradual closure of the corresponding spending-efficiency gap,
for advanced economies, EMDEs and Türkiye.

The closure horizon is 2050 in all three panels. EMDEs and Türkiye also have a
2040 closure, but the advanced-economy set does not, and a slide whose three
panels close their gaps on different dates cannot be read across. The
reallocation-only paths these lines build on are the deck's reallocation slide.
"""
from deck_lines import INFRA, HUMAN_CAPITAL, Panel, Series, Slide, render_slide

INFRA_LABEL = "Infrastructure"
HC_LABEL = "Human capital"

SLIDE = Slide(
    panels=[
        Panel("combinedAE_yd_lines", [
            Series(INFRA_LABEL, "Model_HumanCapital_epsi_igeff25y___yd", INFRA),
            Series(HC_LABEL, "Model_HumanCapital_epsi_cgeeff25y___yd", HUMAN_CAPITAL),
        ]),
        Panel("combinedEM_yd_lines", [
            Series(INFRA_LABEL, "EM_Model_HumanCapital_epsiigeff25y___yd", INFRA),
            Series(HC_LABEL, "EM_Model_HumanCapital_epsicgeeff25y___yd", HUMAN_CAPITAL),
        ]),
        Panel("combinedTR_yd_lines", [
            Series(INFRA_LABEL, "TR_Model_HumanCapital_epsiigeff25y___yd", INFRA),
            Series(HC_LABEL, "TR_Model_HumanCapital_epsicgeeff25y___yd", HUMAN_CAPITAL),
        ]),
    ],
    color_legend=[(INFRA_LABEL, INFRA), (HC_LABEL, HUMAN_CAPITAL)],
)


if __name__ == "__main__":
    render_slide(SLIDE)
