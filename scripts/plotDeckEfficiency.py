"""
Türkiye deck, spending-efficiency slide: the additional output gain over time
from gradually closing spending-efficiency gaps, over and above the
reallocation-only baseline, for advanced economies, EMDEs and Türkiye.

Each line is the efficiency-closing scenario minus its own reallocation
baseline. EMDEs and Türkiye are run at two closure speeds (by 2040 and by
2050); the advanced-economy set has only the 2050 closure, so that panel shows
solid lines alone and drops the dash legend.
"""
from deck_lines import INFRA, HUMAN_CAPITAL, RD, Panel, Series, Slide, render_slide

INFRA_LABEL = "Infrastructure"
HC_LABEL = "Human capital"
RD_LABEL = "R&D"

# No dash legend: at three panels to a slide it costs two legend rows and
# squeezes the plot. The solid/dashed convention is stated in the slide note.
DASH_LEGEND = []

SLIDE = Slide(
    panels=[
        Panel("efficiencyAE_yd_lines", [
            Series(f"{INFRA_LABEL}, closing by 2050", "Model_HumanCapital_epsi_igeff25y___yd",
                   INFRA, base="Model_HumanCapital_epsi_ig___yd"),
            Series(f"{HC_LABEL}, closing by 2050", "Model_HumanCapital_epsi_cgeeff25y___yd",
                   HUMAN_CAPITAL, base="Model_HumanCapital_epsi_cge___yd"),
            Series(f"{RD_LABEL}, closing by 2050", "Model_HumanCapital_epsi_cgrd_eff25y___yd",
                   RD, base="Model_HumanCapital_epsi_cgrd___yd"),
        ], dash_legend=[],
           color_legend=[(INFRA_LABEL, INFRA), (HC_LABEL, HUMAN_CAPITAL), (RD_LABEL, RD)]),
        Panel("efficiencyEM_yd_lines", [
            Series(f"{INFRA_LABEL}, closing by 2050", "EM_Model_HumanCapital_epsiigeff25y___yd",
                   INFRA, base="EM_Model_HumanCapital_epsiig___yd"),
            Series(f"{INFRA_LABEL}, closing by 2040", "EM_Model_HumanCapital_epsiigeff30y___yd",
                   INFRA, dash="dash", base="EM_Model_HumanCapital_epsiig___yd"),
            Series(f"{HC_LABEL}, closing by 2050", "EM_Model_HumanCapital_epsicgeeff25y___yd",
                   HUMAN_CAPITAL, base="EM_Model_HumanCapital_epsicge___yd"),
            Series(f"{HC_LABEL}, closing by 2040", "EM_Model_HumanCapital_epsicgeeff30y___yd",
                   HUMAN_CAPITAL, dash="dash", base="EM_Model_HumanCapital_epsicge___yd"),
        ]),
        Panel("efficiencyTR_yd_lines", [
            Series(f"{INFRA_LABEL}, closing by 2050", "TR_Model_HumanCapital_epsiigeff25y___yd",
                   INFRA, base="TR_Model_HumanCapital_epsiig___yd"),
            Series(f"{INFRA_LABEL}, closing by 2040", "TR_Model_HumanCapital_epsiigeff30y___yd",
                   INFRA, dash="dash", base="TR_Model_HumanCapital_epsiig___yd"),
            Series(f"{HC_LABEL}, closing by 2050", "TR_Model_HumanCapital_epsicgeeff25y___yd",
                   HUMAN_CAPITAL, base="TR_Model_HumanCapital_epsicge___yd"),
            Series(f"{HC_LABEL}, closing by 2040", "TR_Model_HumanCapital_epsicgeeff30y___yd",
                   HUMAN_CAPITAL, dash="dash", base="TR_Model_HumanCapital_epsicge___yd"),
        ]),
    ],
    dash_legend=DASH_LEGEND,
    color_legend=[(INFRA_LABEL, INFRA), (HC_LABEL, HUMAN_CAPITAL)],
)


if __name__ == "__main__":
    render_slide(SLIDE)
