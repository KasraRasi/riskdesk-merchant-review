# How to present RiskDesk in a CPOS interview

## One-minute pitch

"I wanted to understand the actual judgment problem in this role, not just build another fraud classifier. I designed RiskDesk, a small independent prototype using only synthetic merchants, to prioritize reviews based on business-registration evidence, matching bank details, invoice corroboration, sales behavior and disputes. Its output is a transparent review queue with reasons and counterevidence, not an automatic hold. I tested different score thresholds to show the trade-off between catching suspicious patterns and creating friction for legitimate merchants. I also documented cases where KYC passes but business evidence conflicts, and where an innocent seasonal seller spikes in activity."

## Live demonstration (three minutes)

1. Open `outputs/riskdesk_demo.html` in a browser. Start with **M-0001**: passed KYC does not erase multiple conflicting documents and high dispute activity. Read the next-step evidence requests. Explain that the system does not itself freeze money.
2. Search **M-0002**: the simulated event vendor has verified documentation and zero disputes. Discuss why an indiscriminate velocity rule could hurt retention.
3. Search **M-0003**: the new cleaning business has incomplete documentation, not proven fabrication. Describe proportionate evidence requests.
4. Scroll to the threshold table. At 35, 66/360 are sent to review in this toy dataset, including 8 legitimate merchants; nine simulated fraud merchants are missed. Tightening review capacity reduces false alerts but increases missed cases.
5. Close with what you would need to launch in reality: policy/authority, reviewed outcomes, document access, audit trails, calibration, merchant communication and privacy/security review.

## Questions you may get

**Why not just train an ML model?** Because real fraud decisions depend on verified evidence and merchant context. A model may improve triage, but decisions affecting account status need explanations and authorized oversight. The project tests a transparent baseline first.

**Does 88% precision mean your system works in production?** No. The test labels and observed signals were artificially generated together. The metric only illustrates trade-offs, not generalizable performance.

**Why not reject M-0001 immediately?** KYC passing is not proof of a legitimate business, but conflicting evidence is not definitive proof of fraud either. Verification, escalation, an appropriate merchant update and documentation are required.

**What would you track for a real team?** Confirmed loss and dispute outcomes, false-positive reviews, legitimate merchant holds, queue age, merchant time-to-resolution, customer complaints and override patterns.

**How would you improve this?** Connect verified data sources, store an audit trail, add analyst review notes and document request SLAs, run silent backtests, then calibrate policy thresholds with compliance/risk leaders.

## Before sharing as personal work

The working prototype was prepared with AI assistance and is a learning/demo artifact. **Run it, inspect the code and outputs, test three cases, and modify or extend a piece yourself** before saying you built it independently. Be prepared to explain every threshold. Never imply this is a CPOS integration, commercial fraud detection system or validation on real payments data.
