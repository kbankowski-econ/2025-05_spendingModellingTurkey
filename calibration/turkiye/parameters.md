# Türkiye calibration inputs

Source: e-mail from Vybhavi (Bobbi) Balasundharam, 4 August 2026, subject
"RE: Output gains from spending efficiency improvements", saved alongside as
[`2026-08-04_balasundharam_turkiye-parameters.eml`](2026-08-04_balasundharam_turkiye-parameters.eml).

The figures below are the country desk's Türkiye numbers, reported in the same
format as Tables 2 and 4 of the working paper. Model-side names refer to
`models/EM_parameters.macro` and `models/EMnorm_efficiency.macro`.

## Table 2 — steady-state targets

| Reported target | Value | Model parameter | Model value | Current EM | Current AE |
| --- | --- | --- | --- | --- | --- |
| Annual trend output growth | 3.2 % | `g` (gross quarterly) | `1.032^0.25 = 1.007906` | 1.0075 (3.03 %/yr) | 1.004 (1.61 %/yr) |
| Government consumption | 14.0 % of GDP | `Gcy` | 0.14 | 0.14 | 0.18 |
| Infrastructure investment | 4.0 % of GDP | `Igiy` | 0.04 | 0.05 | 0.03 |
| Human capital investment | 3.0 % of GDP | `Igey` | 0.03 | 0.02 | 0.0145 |
| Public R&D spending | 0.4 % of GDP | `Grdy` | 0.004 | 0.001 | 0.006 |
| Consumption tax | 15 % | `taucss` | 0.15 | 0.15 | 0.18 |
| Labor-income tax | 28 % | `tauwss` | 0.28 | 0.10 | 0.25 |
| Public debt level | 30 % of annual GDP | `byss` (quarterly GDP) | `0.30*4 = 1.2` | 2.4 | 4.0 |

Türkiye sits between the EM and AE calibrations: EM-like growth and
consumption taxes, AE-like labor taxation, R&D spending and debt.

## Table 4 — spending efficiency gaps

**The Bankowski et al. 2026 column is the one taken into the model.** The other
two columns are recorded for reference and for the sensitivity check Bobbi
asked about.

As reported (three columns, source-by-source):

| Gap | **Bankowski et al. 2026 (used)** | Fiscal Monitor 2025 | "Average" |
| --- | --- | --- | --- |
| Infrastructure | **0.244** | 0.394 | 0.366 |
| Health | **0.185** | 0.309 | 0.357 |
| Education | **0.278** | 0.328 | 0.381 |
| R&D | **0.457** | 0.434 | 0.434 |

Mapped onto the two model gap parameters. The model carries a single
human-capital gap, so health and education must be collapsed; the simple
average is shown, a spending-weighted average would need the health/education
split of the 3.0 % of GDP human-capital envelope.

| Model parameter | **Bankowski et al. (used)** | Fiscal Monitor | "Average" column | Current EMnorm | Current AE |
| --- | --- | --- | --- | --- | --- |
| `eGI_ss` (infrastructure) | **0.244** | 0.394 | 0.366 | 0.406 | 0.359 |
| `eGE_ss` (human capital, simple avg of health & education) | **0.2315** | 0.3185 | 0.369 | 0.329 | 0.306 |
| `eGRD_ss` (R&D, lives in `*_parameters.macro`) | **0.457** | 0.434 | 0.434 | 0.2 | 0.399 |

On the working-paper estimates Türkiye's infrastructure and human-capital gaps
are *below* the AE calibration, while on the Fiscal Monitor estimates they are
close to the EM calibration.
