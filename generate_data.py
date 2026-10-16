"""Generate entirely synthetic merchant onboarding and transaction-risk examples.

No real businesses, customer identifiers, payment information or platform data.
"""
import csv
import random
from pathlib import Path

SECTORS = ['Food & Market Vendor', 'Home Services', 'Cleaning', 'Professional Services',
           'Mobile Retail', 'Online Goods']

FIELDS = ['merchant_id','sector','merchant_age_days','kyc_status','registration_status',
          'bank_name_match','invoice_evidence','website_or_market_presence',
          'tx_count_30d','disputes_30d','volume_7d_usd','expected_7d_usd',
          'volume_spike_ratio','evidence_note','ground_truth_fraud']


def generate(n=360, seed=42):
    rng = random.Random(seed)
    rows = []
    for idx in range(1, n+1):
        archetype = rng.choices(['normal','seasonal_legit','fraud'],weights=[67,15,18])[0]
        fraud = archetype == 'fraud'
        seasonal = archetype == 'seasonal_legit'
        sector = rng.choice(SECTORS)
        age = rng.randint(1, 65) if fraud else rng.randint(10, 2800)
        if seasonal:
            age = rng.randint(7, 600)
        expected = rng.randint(250, 16000)
        ratio = round(max(0.3, rng.lognormvariate(0, 0.3)), 2)
        if fraud:
            ratio = round(rng.uniform(1.6, 9.5), 2)
        if seasonal:
            ratio = round(rng.uniform(2.8, 8.2), 2)
        volume = round(expected*ratio, 2)
        tx_count = rng.randint(15, 220)
        if fraud:
            tx_count = rng.randint(12, 280)
        disputes = min(tx_count, rng.choices([0, 1, 2, 3, 5, 8, 12],weights=[9,14,20,23,21,9,4])[0]) if fraud else min(tx_count, rng.choices([0,1,2,3],weights=[72,20,7,1])[0])
        bank_match = rng.random() > (0.47 if fraud else 0.055)
        registration = rng.choices(['Verified','Pending clarification','Conflicting'],
                                   weights=[36,28,36] if fraud else [88,10,2])[0]
        invoices = rng.choices(['Verified','Missing / incomplete','Conflicting'],
                               weights=[28,32,40] if fraud else [82,15,3])[0]
        presence = rng.choices(['Established','Limited','None found'],
                               weights=[20,44,36] if fraud else [80,16,4])[0]
        kyc = 'Passed' if rng.random() < (0.90 if fraud else 0.96) else 'Further review'
        if fraud:
            note = rng.choice(['Business footprint is difficult to corroborate.',
                               'Provided invoice details differ across sources.',
                               'Ownership or bank details require confirmation.'])
        elif seasonal:
            note = rng.choice(['Weekend market event explains temporary demand surge.',
                               'Seasonal bookings and event calendar support spike.',
                               'Rapid but documented growth after a local event.'])
        else:
            note = rng.choice(['Ordinary activity for declared business type.',
                               'Supplied business details largely corroborate.',
                               'No material inconsistency identified yet.'])
        rows.append({
            'merchant_id': f'M-{idx:04}', 'sector':sector,
            'merchant_age_days':age,'kyc_status':kyc,'registration_status':registration,
            'bank_name_match':int(bank_match),'invoice_evidence':invoices,
            'website_or_market_presence':presence,'tx_count_30d':tx_count,
            'disputes_30d':disputes,'volume_7d_usd':volume,
            'expected_7d_usd':expected,'volume_spike_ratio':ratio,
            'evidence_note':note,'ground_truth_fraud':int(fraud)})
    # Explicit, human-understandable edge cases - not cherry-picked from the sample.
    exemplars = [
        ('M-0001','Online Goods',12,'Passed','Conflicting',0,'Conflicting','None found',68,9,75000,10000,7.5,'Seller identity passed, but invoices and payout name conflict.',1),
        ('M-0002','Food & Market Vendor',430,'Passed','Verified',1,'Verified','Established',190,0,31000,5500,5.64,'Documented weekend market generated legitimate sales spike.',0),
        ('M-0003','Cleaning',35,'Passed','Pending clarification',1,'Missing / incomplete','Limited',26,0,2700,1700,1.59,'New business: incomplete invoice package; follow up before deciding.',0)
    ]
    for j, item in enumerate(exemplars):
        rows[j] = dict(zip(FIELDS, item))
    return rows


def write_csv(path='data/synthetic_merchants.csv', n=360, seed=42):
    path = Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    rows = generate(n=n,seed=seed)
    with path.open('w',newline='',encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)
    return path

if __name__ == '__main__':
    print(write_csv())
