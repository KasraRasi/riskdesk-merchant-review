# RiskDesk — Case Review & Technical Guide

RiskDesk is a synthetic merchant-risk review prototype. Its aim is to support an evidence-based investigation workflow rather than predict guilt or automatically freeze an account.

**[Open the interactive dashboard](https://kasrarasi.github.io/riskdesk-merchant-review/)**

## Review workflow

1. **Prioritize** a merchant using review points. These points are not probabilities of fraud.
2. **Inspect** the source signals and the counterevidence before drawing conclusions.
3. **Identify gaps** in business registration, payout details, invoices, activity patterns or disputes.
4. **Choose proportional next steps** such as requesting a corroborating document, monitoring or escalating for specialist review.
5. **Document** the rationale and follow-up in the browser-based analyst log. Notes can be exported to CSV.

## Illustrative merchant cases

**M-0001 — Conflicting evidence after KYC approval.** Passing identity verification does not establish that a business is operating legitimately. Conflicting registration, bank and invoice details justify independent verification and possibly escalation, but do not by themselves prove fraud.

**M-0002 — Sales spike with a plausible explanation.** A seasonal or event-related surge can be normal for a legitimate business. Corroborating business evidence and dispute history matter; an indiscriminate velocity rule can create unnecessary merchant friction.

**M-0003 — Incomplete records for a new business.** Missing documentation warrants clarification, not automatic rejection. Appropriate alternative evidence and clear follow-up deadlines may resolve the issue.

## Evaluating review thresholds

The default illustrative threshold is **35 review-priority points**. In the synthetic dataset, that queues **66 of 360** merchants, including **8 legitimate cases**, while missing **9 labelled simulated fraud cases**. The displayed precision and recall are outputs of the constructed dataset, not independent real-world validation.

Moving the threshold changes analyst workload and the trade-off between overlooked risky cases and unnecessary scrutiny of legitimate ones. A production threshold would require cost, capacity and verified-outcome data.

## Implementation and tests

- `generate_data.py` creates deterministic fictional merchant records.
- `core.py` computes rule-based review priority and outcome comparisons.
- `analyze.py` produces the queue and evaluation summaries.
- `dashboard.py` generates the self-contained browser interface.
- `python -m unittest discover -s tests -v` runs seven tests for important scoring and review assumptions.

The interactive site runs entirely in the browser. Review notes use local browser storage and CSV export; they are not submitted to a payments processor or a remote backend.

## What would be required for production

Verified identity and business-document sources, analyst roles and approvals, retained decision records, secure persistence, dispute/chargeback integration, calibrated thresholds using independently confirmed outcomes, measurable merchant friction, privacy/security controls, and documented escalation authority.

The project uses synthetic cases, contains no operational financial data, and is not affiliated with CPOS. AI-assisted tools were used during development; the prototype is intended for review, testing and further iteration rather than operational decision-making.