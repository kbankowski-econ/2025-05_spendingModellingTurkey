"""
Türkiye deck, reallocation slide: output gains over time from a permanent
reallocation of 1 percent of GDP away from public consumption, for advanced
economies, EMDEs and Türkiye.

Three panels sharing one y-range. EMDEs and Türkiye have no R&D reallocation
experiment, so those panels carry two lines rather than three.
"""
from deck_lines import INFRA, HUMAN_CAPITAL, RD, Panel, Series, Slide, render_slide

INFRA_LABEL = "Infrastructure"
HC_LABEL = "Human capital"
RD_LABEL = "R&D"

SLIDE = Slide(
    panels=[
        Panel("reallocationAE_yd_lines", [
            Series(INFRA_LABEL, "Model_HumanCapital_epsi_ig___yd", INFRA),
            Series(HC_LABEL, "Model_HumanCapital_epsi_cge___yd", HUMAN_CAPITAL),
            Series(RD_LABEL, "Model_HumanCapital_epsi_cgrd___yd", RD),
        ]),
        Panel("reallocationEM_yd_lines", [
            Series(INFRA_LABEL, "EM_Model_HumanCapital_epsiig___yd", INFRA),
            Series(HC_LABEL, "EM_Model_HumanCapital_epsicge___yd", HUMAN_CAPITAL),
        ]),
        Panel("reallocationTR_yd_lines", [
            # Türkiye's two endpoints nearly coincide (4.8 versus 4.9); the
            # renderer separates their value labels.
            Series(INFRA_LABEL, "TR_Model_HumanCapital_epsiig___yd", INFRA),
            Series(HC_LABEL, "TR_Model_HumanCapital_epsicge___yd", HUMAN_CAPITAL),
        ]),
    ],
)


if __name__ == "__main__":
    render_slide(SLIDE)
