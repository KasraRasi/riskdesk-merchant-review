"""Transparent rules for MERCHANT REVIEW PRIORITY, not automated accusations.

The policy intentionally abstains: it prioritizes cases for a qualified human reviewer.
"""
from dataclasses import dataclass

@dataclass
class Assessment:
    score: int
    priority: str
    reasons: list
    counterevidence: list
    next_steps: list
    human_review_required: bool = True


def assess(row):
    reasons = []
    counter = []
    steps = []
    score = 0
    age = int(row['merchant_age_days'])
    spike = float(row['volume_spike_ratio'])
    transactions = max(1,int(row['tx_count_30d']))
    disputes = int(row['disputes_30d'])
    dispute_rate = disputes/transactions
    bank_match = str(row['bank_name_match']).lower() in ('1','true','yes')
    if row['registration_status'] == 'Conflicting':
        score += 30; reasons.append('Registration evidence conflicts with declared details')
        steps.append('Verify registration independently and request consistent legal business name')
    elif row['registration_status'] == 'Pending clarification':
        score += 9; reasons.append('Registration information needs clarification')
        steps.append('Request updated registration or reasonable alternate evidence')
    else:
        counter.append('Business registration corroborated')
    if not bank_match:
        score += 22; reasons.append('Bank account name does not match submitted business details')
        steps.append('Confirm authorized payout beneficiary with secure verification workflow')
    else:
        counter.append('Bank name matches supplied business details')
    if row['invoice_evidence'] == 'Conflicting':
        score += 23; reasons.append('Invoice evidence contradicts supplied details')
        steps.append('Verify invoice context, counterparties and authenticity')
    elif row['invoice_evidence'] == 'Missing / incomplete':
        score += 7; reasons.append('Invoice evidence is missing or incomplete')
        steps.append('Ask for invoice or alternative proof of genuine trading')
    else:
        counter.append('Invoice evidence corroborated')
    if row['website_or_market_presence'] == 'None found':
        score += 10; reasons.append('Independent business footprint not established')
        steps.append('Check alternative proof (market permits, service bookings or supplier records)')
    elif row['website_or_market_presence'] == 'Established':
        counter.append('Independent business footprint corroborated')
    if age < 30:
        score += 7; reasons.append('Recently established merchant')
    if spike >= 5:
        score += 18; reasons.append(f'7-day volume {spike:.1f}x expected level')
        steps.append('Ask whether seasonality, events or recent promotions explain activity')
    elif spike >= 3:
        score += 9; reasons.append(f'7-day volume {spike:.1f}x expected level')
    if dispute_rate >= 0.06 and disputes >= 2:
        score += 22; reasons.append(f'Elevated disputes: {disputes}/{transactions} ({100*dispute_rate:.1f}%)')
        steps.append('Inspect dispute reasons and exposure; preserve evidence for disputes')
    elif disputes > 0 and dispute_rate >= 0.025:
        score += 10; reasons.append(f'Disputes require monitoring: {100*dispute_rate:.1f}%')
    elif disputes == 0:
        counter.append('No recorded disputes in the 30-day synthetic window')
    if row['kyc_status'] == 'Passed':
        counter.append('Individual identity verification passed; business legitimacy still needs review')
    else:
        score += 10; reasons.append('Individual identity verification requires follow-up')
        steps.append('Resolve identity verification issue')
    # Transparent review bands. No automatic reject or funds movement.
    if score >= 70:
        priority = 'High - urgent human review'
    elif score >= 35:
        priority = 'Medium - investigate'
    else:
        priority = 'Low - routine review'
    if not steps:
        steps = ['Confirm the observed pattern fits the merchant business model',
                 'Record rationale and set proportionate monitoring']
    return Assessment(score,priority,reasons,counter,list(dict.fromkeys(steps)))


def flagged(row, threshold=35):
    return assess(row).score >= threshold


def metrics(rows,threshold=35):
    tp=fp=fn=tn=0
    for row in rows:
        actual = bool(int(row['ground_truth_fraud']))
        predicted = flagged(row,threshold)
        if actual and predicted: tp+=1
        elif not actual and predicted: fp+=1
        elif actual and not predicted: fn+=1
        else: tn+=1
    total = tp+fp+fn+tn
    return {
        'threshold':threshold,'n':total,'tp':tp,'fp':fp,'fn':fn,'tn':tn,
        'precision':round(tp/(tp+fp),4) if tp+fp else 0,
        'recall':round(tp/(tp+fn),4) if tp+fn else 0,
        'specificity':round(tn/(tn+fp),4) if tn+fp else 0,
        'review_queue':tp+fp,
        'review_rate':round((tp+fp)/total,4) if total else 0
    }
