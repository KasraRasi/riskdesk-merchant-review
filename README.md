# RiskDesk · Merchant Risk Review Lab

**Interactive payments-risk portfolio prototype · Synthetic merchant data · No production integrations**

RiskDesk explores a practical problem in merchant onboarding and monitoring: how to prioritize suspicious cases, verify conflicting business evidence, and avoid unnecessary disruption to legitimate merchants. It combines transparent review-priority rules with an interactive queue, evidence summaries and an analyst decision log.

**[Open the live dashboard](https://kasrarasi.github.io/riskdesk-merchant-review/)** · [View the source code](https://github.com/KasraRasi/riskdesk-merchant-review)

![RiskDesk dashboard](assets/dashboard_preview.png)

## Capabilities

- Browse and filter **360 reproducible synthetic merchants** by priority, sector or ID.
- Examine onboarding and monitoring evidence: KYC status, business-registration consistency, payout-bank-name checks, invoices, transaction-volume changes and dispute activity.
- Compare reasons for concern with plausible benign explanations before choosing proportionate verification steps.
- Record an analyst review status and rationale; export review notes as CSV. Notes remain in the browser, not on a server.
- Compare six review thresholds against synthetic outcomes to illustrate false-positive workload and missed-case trade-offs.

**Scope:** risk points represent *review priority*, not a fraud probability. The prototype cannot hold funds, decline accounts or take other actions against merchants.

## Three cases to explore

| Case | Evidence to consider | Analyst question |
|---|---|---|
| `M-0001` | KYC passed, but business documents and payout details conflict; disputes are elevated | What independent evidence is needed before escalation? |
| `M-0002` | Established seller with a temporary activity spike and corroborating evidence | Is the surge consistent with the business rather than fraud? |
| `M-0003` | New service business with incomplete—but not contradictory—documents | What proportionate follow-up can resolve the gaps? |

See the [case review guide](PROJECT_WALKTHROUGH.md) and [case notes](outputs/case_bank.md) for interpretation and limitations.

## Run locally

For the interactive demonstration, download the repository and open `index.html` in a browser. The dashboard works offline and needs no Python installation or account.

To regenerate the dataset, evaluations and dashboard, use **Python 3.9+**:

```powershell
python generate_data.py
python analyze.py
python -m unittest discover -s tests -v
python dashboard.py
```

Copy `outputs/riskdesk_demo.html` to `index.html` after regeneration if you want to update the published site. The included `rebuild_windows.bat` runs the analysis and dashboard steps on Windows with the `py` launcher.

## Repository layout

| File | Purpose |
|---|---|
| `index.html` | Standalone live dashboard for GitHub Pages |
| `generate_data.py` | Reproducible synthetic merchant data |
| `core.py` | Explainable scoring and evaluation logic |
| `analyze.py` | Queue, metrics and threshold comparisons |
| `dashboard.py` | Dashboard HTML generator |
| `data/`, `outputs/` | Synthetic records and analysis artifacts |
| `tests/` | Seven unit tests for policy and scoring assumptions |
| `PROJECT_WALKTHROUGH.md` | Short case review and technical guide |

## Assumptions and limitations

This is a **synthetic demonstration**, not a real merchant underwriting system or a CPOS integration. All cases, labels and outcomes are simulated; reported precision and recall are illustrative and **cannot be generalized to real fraud detection**. The site contains no real identities, payment credentials or company data.

The prototype does not implement document authentication, production KYC/KYB, secure multi-user case storage, dispute recovery, regulatory controls or account actions. A real deployment would need independently sourced evidence, authorization policies, an audit trail, compliance review and prospective evaluation. Development included AI-assisted tooling; analysis and technical claims should be reviewed and tested before reuse.