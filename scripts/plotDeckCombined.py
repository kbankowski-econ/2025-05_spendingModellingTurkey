"""
Türkiye deck, combined slide: output gains from reallocation alone (solid) and
from reallocation together with a gradual closure of the corresponding
spending-efficiency gap (dashed), for advanced economies, EMDEs and Türkiye.

The closure horizon is 2050 in all three panels. EMDEs and Türkiye also have a
2040 closure, but the advanced-economy set does not, and a slide whose three
panels close their gaps on different dates cannot be read across.
"""
from deck_lines import INFRA, HUMAN_CAPITAL, Panel, Series, Slide, render_slide

INFRA_LABEL = "Infrastructure"
HC_LABEL = "Human capital"

SLIDE = Slide(
    panels=[
        Panel("combinedAE_yd_lines", [
            Series(f"{INFRA_LABEL}: reallocation", "Model_HumanCapital_epsi_ig___yd",
                   INFRA),
            Series(f"{HC_LABEL}: reallocation", "Model_HumanCapital_epsi_cge___yd",
                   HUMAN_CAPITAL),
            Series(f"{INFRA_LABEL}: reallocation and efficiency by 2050",
                   "Model_HumanCapital_epsi_igeff25y___yd", INFRA, dash="dash"),
            Series(f"{HC_LABEL}: reallocation and efficiency by 2050",
                   "Model_HumanCapital_epsi_cgeeff25y___yd", HUMAN_CAPITAL, dash="dash"),
        ]),
        Panel("combinedEM_yd_lines", [
            Series(f"{INFRA_LABEL}: reallocation", "EM_Model_HumanCapital_epsiig___yd",
                   INFRA),
            Series(f"{HC_LABEL}: reallocation", "EM_Model_HumanCapital_epsicge___yd",
                   HUMAN_CAPITAL),
            Series(f"{INFRA_LABEL}: reallocation and efficiency by 2050",
                   "EM_Model_HumanCapital_epsiigeff25y___yd", INFRA, dash="dash"),
            Series(f"{HC_LABEL}: reallocation and efficiency by 2050",
                   "EM_Model_HumanCapital_epsicgeeff25y___yd", HUMAN_CAPITAL, dash="dash"),
        ]),
        Panel("combinedTR_yd_lines", [
            # The two reallocation endpoints nearly coincide under the Türkiye
            # calibration; the renderer separates their value labels.
            Series(f"{INFRA_LABEL}: reallocation", "TR_Model_HumanCapital_epsiig___yd",
                   INFRA),
            Series(f"{HC_LABEL}: reallocation", "TR_Model_HumanCapital_epsicge___yd",
                   HUMAN_CAPITAL),
            Series(f"{INFRA_LABEL}: reallocation and efficiency by 2050",
                   "TR_Model_HumanCapital_epsiigeff25y___yd", INFRA, dash="dash"),
            Series(f"{HC_LABEL}: reallocation and efficiency by 2050",
                   "TR_Model_HumanCapital_epsicgeeff25y___yd", HUMAN_CAPITAL, dash="dash"),
        ]),
    ],
    # No dash legend: at three panels to a slide it costs two legend rows and
    # squeezes the plot. The solid/dashed convention is stated in the slide note.
    dash_legend=[],
    color_legend=[(INFRA_LABEL, INFRA), (HC_LABEL, HUMAN_CAPITAL)],
)


if __name__ == "__main__":
    render_slide(SLIDE)
