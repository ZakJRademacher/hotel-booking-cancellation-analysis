from pathlib import Path
import csv,importlib.util,sqlite3,unittest
P=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('refresh',P/'refresh.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class HotelChecks(unittest.TestCase):
    def test_band_boundaries(self):
        self.assertEqual([m.lead_band(x)[:2] for x in [0,7,8,30,31,90,91,180,181]],['01','01','02','02','03','03','04','04','05'])
        with self.assertRaises(ValueError):m.lead_band(-1)
    def test_independent_source_totals(self):
        with (P/'data/raw/hotel_bookings.csv').open(encoding='utf-8-sig') as f:
            rows=[r for r in csv.DictReader(f) if r['arrival_date_year']=='2016']
        self.assertEqual(len(rows),56707);self.assertEqual(sum(int(r['is_canceled']) for r in rows),20337)
        self.assertEqual(sum((int(r['stays_in_week_nights'])+int(r['stays_in_weekend_nights']))*int(r['is_canceled']) for r in rows),69421)
    def test_each_dashboard_view_reconciles(self):
        with (P/'tableau/Data/analysis.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
        for view in ['segments','rate','lead','trend','kpi']:
            pop=[r for r in rows if r['View']==view and r['Year']=='2016' and r['Hotel']=='City Hotel']
            self.assertEqual(sum(int(r['Bookings']) for r in pop),38140)
            self.assertEqual(sum(int(r['Value']) for r in pop),15407)
    def test_source_lineage_and_empty_selection(self):
        db=sqlite3.connect(P/'data/processed/analysis.sqlite')
        self.assertEqual(db.execute('SELECT COUNT(*),COUNT(DISTINCT source_row) FROM bookings').fetchone(),(119390,119390))
        self.assertEqual(db.execute("SELECT COUNT(*) FROM bookings WHERE year='2014'").fetchone()[0],0)
        self.assertEqual(db.execute('SELECT COUNT(*) FROM bookings WHERE canceled_nights > nights OR nights<0').fetchone()[0],0)

if __name__=='__main__':unittest.main()
