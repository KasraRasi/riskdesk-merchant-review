import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
from generate_data import generate
from core import assess, metrics

class TestRiskEngine(unittest.TestCase):
    def test_dataset_deterministic(self):
        self.assertEqual(generate(20,42),generate(20,42))
    def test_kyc_pass_is_not_auto_approval(self):
        rows=generate()
        flagged=assess(rows[0])
        self.assertEqual(rows[0]['kyc_status'],'Passed')
        self.assertGreaterEqual(flagged.score,70)
        self.assertTrue(flagged.human_review_required)
    def test_seasonal_merchant_not_flagged_from_spike_alone(self):
        r=generate()[1]
        a=assess(r)
        self.assertEqual(r['ground_truth_fraud'],0)
        self.assertLess(a.score,35)
    def test_incomplete_docs_are_not_an_automatic_decline(self):
        r=generate()[2]
        a=assess(r)
        self.assertLess(a.score,35)
        self.assertTrue(a.human_review_required)
    def test_conflicting_docs_increase_score(self):
        r=dict(generate()[2]); base=assess(r).score
        r['invoice_evidence']='Conflicting'; self.assertGreater(assess(r).score,base)
    def test_metrics_totals(self):
        m=metrics(generate(100),35)
        self.assertEqual(m['tp']+m['fp']+m['tn']+m['fn'],100)
    def test_more_review_fewer_false_negatives(self):
        rows=generate()
        self.assertLessEqual(metrics(rows,25)['fn'],metrics(rows,70)['fn'])

if __name__=='__main__':unittest.main()
