# RiskDesk case bank: examples of written merchant-risk reasoning

Independent portfolio demonstration — **all merchants, documents, and activity are synthetic**. These are practice examples, not actual CPOS cases. Reviewers should verify independently, apply company policy and document decisions.

## M-0001 — Conflicting evidence despite passed identity check

**Decision at intake:** Escalate for urgent human review. **Do not interpret the prototype score as authority to freeze funds, reject a merchant, or make an accusation.**

**Signals:** KYC is passed, but business registration is conflicting; payout bank name does not match; invoices are inconsistent; no independent footprint is found; seven-day volume is 7.5 times expectation; 9 of 68 transactions have disputes in this simulation.

**What the signals do not establish:** They do not individually prove intentional deception. There could be an authorized representative, DBA/trade name, business transition, faulty source mapping, or incomplete paperwork. Investigate each plausible explanation without losing sight of the compound risk.

**Next steps:** Request legal entity/registration evidence and a documented connection between payout account and business. Validate invoice sources securely. Review timing, age and reason codes of disputes, and compare activity against declared goods/services. Escalate under authorized risk policy. Record what changed the decision.

**Example merchant note:**

> Thank you for the information provided. We're reviewing a few details so that we can confirm your business and payout information match. Please provide an updated registration document and documentation showing the relationship between the business and nominated bank account through our secure verification process. We'll review the information and provide a status update as soon as we can. Please avoid sending account credentials or sensitive banking information over email.

## M-0002 — High activity but a legitimate seasonal merchant

**Decision at intake:** Routine review / approve subject to real policy, with proportionate monitoring; no special hold justified *solely* by the spike.

**Signals:** KYC and business registration pass, payout bank name matches, invoice evidence is verified, the merchant has an established business footprint and no disputes. The 5.64x volume spike has a documented weekend market event explanation.

**Analyst rationale:** A volume-only rule could flag a legitimate small merchant and delay access to money needed to restock. Seek an explanation consistent with the merchant type, corroborate it and update the expected-activity baseline where warranted.

**Rule feedback:** Add a seasonal-event contextual review before escalating otherwise clean merchants purely on spikes. Test new logic on both event merchants and lookalike fraud cases; log overrides to monitor unintended misses.

## M-0003 — New business with incomplete documents

**Decision at intake:** Request clarification rather than reject. Evidence is incomplete, not contradictory.

**Signals:** 35-day-old cleaning company, KYC passed, bank name matched, registration pending clarification, invoices missing or incomplete, no disputes and a modest 1.59x increase in activity.

**Next steps:** Ask for alternative evidence appropriate for a sole proprietor (e.g., appointment invoices, service agreement or municipal registration if relevant). Check whether the document standard is proportionate for a newly formed business. Record the source of any unresolved concern and provide the merchant a clear follow-up path.

## Learning loop / control notes

- Capture reasons and counterevidence as separate fields; a single score is not an explanation.
- Track **false positives** (legitimate merchants sent for review), **false negatives** (confirmed fraud not reviewed), queue aging, wait time, merchant complaints, dispute rates and verified outcomes.
- Keep identity verification (KYC), business verification (KYB), transaction behavior and payout authority conceptually distinct.
- Evaluate case decisions over time without training on outcomes that were only possible because the system selected who got reviewed (selection bias).
- Avoid collecting unnecessary personally identifiable information and never use email for credentials or banking secrets.
