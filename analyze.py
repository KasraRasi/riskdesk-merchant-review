"""Run deterministic synthetic evaluation and export model-independent evidence."""
import csv, json
from pathlib import Path
from generate_data import write_csv
from core import assess, metrics

ROOT = Path(__file__).resolve().parent
DATA = ROOT/'data'/'synthetic_merchants.csv'
OUT = ROOT/'outputs'

def main():
    write_csv(DATA)
    with DATA.open(encoding='utf-8',newline='') as f:
        rows = list(csv.DictReader(f))
    OUT.mkdir(exist_ok=True)
    thresholds = [25,35,45,55,70,85]
    results = [metrics(rows,t) for t in thresholds]
    with (OUT/'evaluation.json').open('w',encoding='utf-8') as f:
        json.dump({'synthetic_only':True,'dataset_size':len(rows),'threshold_results':results,
                   'threshold_selection':'35 is illustrative and NOT calibrated on real loss outcomes; review queue rather than decline automation.'},f,indent=2)
    with (OUT/'review_queue.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['merchant_id','sector','priority','score','top_reasons','suggested_next_steps'])
        writer.writeheader()
        for r in sorted(rows,key=lambda x:assess(x).score,reverse=True):
            a=assess(r)
            writer.writerow({'merchant_id':r['merchant_id'],'sector':r['sector'],'priority':a.priority,
                             'score':a.score,'top_reasons':' | '.join(a.reasons[:3]),
                             'suggested_next_steps':' | '.join(a.next_steps[:2])})
    print(json.dumps(results,indent=2))
    for key in ['M-0001','M-0002','M-0003']:
        r=next(x for x in rows if x['merchant_id']==key)
        a=assess(r)
        print(key, a.score, a.priority, '|',a.reasons)
    return rows,results

if __name__=='__main__':
    main()
