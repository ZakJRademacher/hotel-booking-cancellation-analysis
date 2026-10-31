"""Validate the pinned hotel source and build booking-grain reporting data."""
from pathlib import Path
import calendar,csv,hashlib,json,sqlite3
from datetime import date

ROOT=Path(__file__).resolve().parent

def lead_band(days):
    if days<0: raise ValueError('Negative lead time')
    return '01  0-7 days' if days<=7 else '02  8-30 days' if days<=30 else '03  31-90 days' if days<=90 else '04  91-180 days' if days<=180 else '05  181+ days'

def refresh(root=ROOT):
    source=root/'data/raw/hotel_bookings.csv'
    expected=json.loads((root/'data/source-download.json').read_text())['files'][0]['sha256']
    assert hashlib.sha256(source.read_bytes()).hexdigest()==expected,'Source fingerprint changed; review before publication'
    output=root/'data/processed';output.mkdir(parents=True,exist_ok=True)
    records=[]; repeats=set();repeat_count=0
    with source.open(encoding='utf-8-sig',newline='') as stream:
        reader=csv.DictReader(stream)
        assert len(reader.fieldnames)==len(set(reader.fieldnames))
        for rowno,row in enumerate(reader,2):
            assert None not in row and None not in row.values(),'Malformed CSV row'
            raw=tuple(row.values());repeat_count+=raw in repeats;repeats.add(raw)
            arrival=date(int(row['arrival_date_year']),list(calendar.month_name).index(row['arrival_date_month']),int(row['arrival_date_day_of_month']))
            canceled=int(row['is_canceled']);assert canceled in (0,1)
            lead=int(row['lead_time']);nights=int(row['stays_in_weekend_nights'])+int(row['stays_in_week_nights']);assert nights>=0
            records.append((rowno,row['hotel'],arrival.isoformat(),arrival.strftime('%Y-%m'),str(arrival.year),row['market_segment'].strip() or 'Unknown',lead,lead_band(lead),canceled,nights,nights*canceled))
    assert len(records)==119390
    db=sqlite3.connect(':memory:')
    db.execute('CREATE TABLE bookings(source_row INTEGER PRIMARY KEY,hotel TEXT,arrival TEXT,period TEXT,year TEXT,segment TEXT,lead_days INTEGER,lead_band TEXT,canceled INTEGER,nights INTEGER,canceled_nights INTEGER)')
    db.executemany('INSERT INTO bookings VALUES (?,?,?,?,?,?,?,?,?,?,?)',records)
    headers=['Source Row','Hotel','Arrival','Period','Year','Segment','Lead Days','Lead Band','Canceled','Booked Nights','Canceled Booked Nights']
    with (output/'Bookings.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(headers);writer.writerows(records)
    controls={}
    for key,where in [('all','1=1'),('2016',"year='2016'"),('2016_city',"year='2016' AND hotel='City Hotel'"),('2016_resort',"year='2016' AND hotel='Resort Hotel'")]:
        n,c,bn,cn=db.execute('SELECT COUNT(*),SUM(canceled),SUM(nights),SUM(canceled_nights) FROM bookings WHERE '+where).fetchone()
        controls[key]={'bookings':n,'cancellations':c,'rate':c/n,'booked_nights':bn,'canceled_booked_nights':cn}
    for group in ['segment','lead_band','period']:
        query=f'SELECT hotel,{group},COUNT(*) bookings,SUM(canceled) cancellations,1.0*SUM(canceled)/COUNT(*) cancellation_rate,SUM(canceled_nights) canceled_booked_nights FROM bookings WHERE year=\'2016\' GROUP BY hotel,{group} ORDER BY cancellations DESC'
        cur=db.execute(query)
        with (output/(group+'-2016.csv')).open('w',newline='',encoding='utf-8') as stream:
            w=csv.writer(stream);w.writerow([x[0] for x in cur.description]);w.writerows(cur)
    # All combinations support matched-month comparisons, not pooled causal claims.
    cur=db.execute('SELECT hotel,period,segment,lead_band,COUNT(*) bookings,SUM(canceled) cancellations,SUM(canceled_nights) canceled_booked_nights FROM bookings GROUP BY hotel,period,segment,lead_band')
    with (output/'comparison-cells.csv').open('w',newline='',encoding='utf-8') as stream:
        w=csv.writer(stream);w.writerow([x[0] for x in cur.description]);w.writerows(cur)
    controls.update(source_rows=len(records),exact_repeats_retained=repeat_count,source_sha256=expected,reporting_sha256=hashlib.sha256((output/'Bookings.csv').read_bytes()).hexdigest())
    (output/'controls.json').write_text(json.dumps(controls,indent=2)+'\n')
    temporary=output/'analysis.next.sqlite'
    db.commit();dest=sqlite3.connect(temporary);db.backup(dest);dest.close();temporary.replace(output/'analysis.sqlite')
    print(json.dumps(controls,indent=2))
    return controls

if __name__=='__main__':refresh()
