"""Build native Tableau views over a validated, filterable reporting cube."""
from pathlib import Path
import csv,sqlite3,json,copy,zipfile,xml.etree.ElementTree as E
import tableau_builder as b

P=Path(__file__).resolve().parents[1]

def build():
    db=sqlite3.connect(P/'data/processed/analysis.sqlite')
    b.FIELDS=[('View','string'),('Label','string'),('Series','string'),('Value','real'),('Sort','integer'),('Note','string'),('Bookings','integer'),('Canceled Nights','integer'),('Hotel','string'),('Year','string'),('Period','string'),('Segment','string')]
    rows=[]
    for view,group in [('segments','segment'),('rate','segment'),('lead','lead_band'),('trend','period'),('kpi','hotel')]:
        q=f'SELECT hotel,year,period,segment,{group},COUNT(*),SUM(canceled),SUM(canceled_nights) FROM bookings GROUP BY hotel,year,period,segment,{group}'
        for hotel,year,period,segment,label,n,c,cn in db.execute(q):
            rows.append([view,label,'Cancellations',c,0,'Historical observations; not an intervention effect',n,cn,hotel,year,period,segment])
    charts=[('Cancellation workload','segments','01  Cancellations by market segment','Bar',24,370,655,240),('Segment rate','rate','02  Cancellation rate by segment','Bar',704,370,672,240),('Lead-time rate','lead','03  Rate by lead-time band','Bar',24,630,655,170),('Monthly rate','trend','04  Monthly cancellation rate (YYMM)','Line',704,630,672,170)]
    path=b.tableau(P/'tableau','Hotel Cancellation Review',rows,'Where should reservations test better confirmation?',
        'Default: 2016, City Hotel / Change the filters to compare the same hotel and arrival period.',
        [('Bookings','',''),('Cancellations','',''),('Cancellation rate','','')],charts,
        'Compare counts and rates together. Prioritize a confirmation-process trial, then measure results against a randomized comparison group.',
        'Kaggle / Antonio, de Almeida & Nunes (2019), CC BY 4.0 / Partial 2015 and 2017 / Zak Rademacher')
    tree=E.parse(path);book=tree.getroot();ds=book.find('./datasources/datasource')
    rate=E.SubElement(ds,'column',{'name':'[Cancellation Rate]','datatype':'real','role':'measure','type':'quantitative','default-format':'p0.0%'})
    E.SubElement(rate,'calculation',{'class':'tableau','formula':'IF SUM([Bookings]) > 0 THEN SUM([Value]) / SUM([Bookings]) END'})
    for c in ds.findall('column'):
        if c.get('name') in ['[Value]','[Bookings]','[Canceled Nights]']:c.set('default-format','n#,##0')
    for sheet in book.findall('./worksheets/worksheet'):
        view=sheet.find('./table/view');deps=view.find('datasource-dependencies')
        deps.append(copy.deepcopy(rate));E.SubElement(deps,'column-instance',{'column':'[Cancellation Rate]','derivation':'User','name':'[usr:Cancellation Rate:qk]','pivot':'key','type':'quantitative'})
        for field,member in [('Hotel','City Hotel'),('Year','2016')]:
            f=E.SubElement(view,'filter',{'class':'categorical','column':f'[analysis].[none:{field}:nk]'})
            E.SubElement(f,'groupfilter',{'function':'member','level':f'[none:{field}:nk]','member':json.dumps(member)})
            E.SubElement(view.find('slices'),'column').text=f'[analysis].[none:{field}:nk]'
        if sheet.get('name')!='Cancellation workload':
            for el in sheet.iter():
                if el.text and '[analysis].[sum:Value:qk]' in el.text:el.text=el.text.replace('[analysis].[sum:Value:qk]','[analysis].[usr:Cancellation Rate:qk]')
                for k,v in list(el.attrib.items()):
                    if '[analysis].[sum:Value:qk]' in v:el.set(k,v.replace('[analysis].[sum:Value:qk]','[analysis].[usr:Cancellation Rate:qk]'))
        for f in sheet.findall('.//style-rule[@element="axis"]/format[@attr="title"]'):f.set('value','Cancellations' if sheet.get('name')=='Cancellation workload' else 'Cancellation rate')
        tooltip=sheet.find('.//customized-tooltip/formatted-text/run');tooltip.text='<[analysis].[none:Label:nk]>\nBookings: <[analysis].[sum:Bookings:qk]>\nCancellations: <[analysis].[sum:Value:qk]>\nRate: <[analysis].[usr:Cancellation Rate:qk]>\nCanceled booked nights: <[analysis].[sum:Canceled Nights:qk]>'
        enc=sheet.find('./table/panes/pane/encodings')
        for col in ['[analysis].[sum:Bookings:qk]','[analysis].[sum:Canceled Nights:qk]','[analysis].[sum:Value:qk]','[analysis].[usr:Cancellation Rate:qk]']:E.SubElement(enc,'tooltip',{'column':col})
    dash=book.find('./dashboards/dashboard');zones=dash.find('./zones/zone')
    # Replace fixed KPI text with native measure worksheets sharing the same filters.
    for z in list(zones):
        y=int(z.get('y','0'))
        if 16000<=y<=32000 or z.get('type')=='color':zones.remove(z)
    base=copy.deepcopy(book.find('./worksheets/worksheet'))
    for idx,(name,measure) in enumerate([('Selected bookings','Bookings'),('Selected cancellations','Value'),('Selected rate','Cancellation Rate'),('Canceled booked nights','Canceled Nights')]):
        s=copy.deepcopy(base);s.set('name',name)
        v=s.find('./table/view');v.find('filter/groupfilter').set('member','"kpi"')
        for sort in list(v.findall('sort')):v.remove(sort)
        pane=s.find('./table/panes/pane');pane.find('mark').set('class','Text');enc=pane.find('encodings');enc.clear()
        ref='[analysis].[usr:Cancellation Rate:qk]' if measure=='Cancellation Rate' else f'[analysis].[sum:{measure}:qk]'
        E.SubElement(enc,'text',{'column':ref});s.find('./table/rows').text='';s.find('./table/cols').text=''
        for run in s.findall('./layout-options/title/formatted-text/run'):run.text=name
        for fmt in s.findall('.//style-rule[@element="mark"]/format'):
            if fmt.get('attr')=='mark-labels-show':fmt.set('value','true')
        rule=E.SubElement(pane.find('style'),'style-rule',{'element':'mark'});E.SubElement(rule,'format',{'attr':'font-size','value':'26'})
        book.find('worksheets').append(s)
        E.SubElement(zones,'zone',{'id':str(100+idx),'name':name,'show-title':'true','x':str(int((24+idx*350)/1400*100000)),'y':'27000','w':'23500','h':'10000'})
        win=copy.deepcopy(book.find('./windows/window[@class="worksheet"]'));win.set('name',name);book.find('windows').append(win)
        E.SubElement(E.SubElement(book.find('./windows/window[@class="dashboard"]/viewpoints'),'viewpoint',{'name':name}),'zoom',{'type':'entire-view'})
    # Controls scoped to all worksheets use the native source filter association.
    for idx,(field,label) in enumerate([('Hotel','Hotel'),('Year','Arrival year'),('Period','Arrival month'),('Segment','Market segment')]):
        E.SubElement(zones,'zone',{'id':str(120+idx),'type':'filter','name':'Cancellation workload','param':f'[analysis].[none:{field}:nk]','mode':'dropdown','values':'all','x':str(int((24+idx*350)/1400*100000)),'y':'17500','w':'23500','h':'8500'})
    # Global filter declarations keep every sheet in the same population.
    for field in ['Hotel','Year','Segment']:
        gf=E.SubElement(book,'filter-group',{'name':field})
        for s in book.findall('./worksheets/worksheet'):E.SubElement(gf,'filter',{'column':f'[analysis].[none:{field}:nk]','worksheet':s.get('name')})
    # Separate method dashboard contains no filter-sensitive numerical claims.
    method=copy.deepcopy(dash);method.set('name','02  Definitions and trial');mz=method.find('./zones/zone');mz.clear();mz.set('id','1');mz.set('type','layout-basic');mz.set('x','0');mz.set('y','0');mz.set('w','100000');mz.set('h','100000')
    sections=[('A bounded decision for reservations',40,32,28),('Choose a comparable hotel and arrival period, then examine market-segment counts and rates. Use lead-time bands to define a trial population. Small samples below 100 bookings need caution.',140,180,16),('Population and measures',350,46,22),('One source row represents one booking. Cancellation rate = canceled bookings / bookings in the same selection. Canceled booked nights = recorded length of stay on canceled bookings. Those nights are not proven lost revenue or unfilled capacity. Exact repeats remain because the source has no booking identifier.',420,180,16),('Test the recommendation',640,46,22),('Within a selected hotel, segment and lead-time band, randomize an improved confirmation protocol against business-as-usual. Measure cancellation rate, staff contact workload and guest complaints. The historical snapshot cannot establish a treatment effect. Reservation fields reflect the source extraction snapshot, not guaranteed initial-booking knowledge.',710,180,16)]
    for i,(text,y,h,size) in enumerate(sections):
        z=E.SubElement(mz,'zone',{'id':str(200+i),'type':'text','x':'2000','y':str(int(y/950*100000)),'w':'95000','h':str(int(h/950*100000))});f=E.SubElement(z,'formatted-text');E.SubElement(f,'run',{'fontname':'Segoe UI','fontsize':str(size),'fontcolor':b.INK}).text=text
    book.find('dashboards').append(method);win=E.SubElement(book.find('windows'),'window',{'name':method.get('name'),'class':'dashboard','maximized':'true'});E.SubElement(win,'active',{'id':'-1'})
    # Tableau's XML content models require columns before style, filters before
    # sorting/slices, zone styles last, and cards/viewpoints on every window.
    ds.remove(rate);ds.insert(list(ds).index(ds.find('style')),rate)
    for sheet in book.findall('./worksheets/worksheet'):
        view=sheet.find('./table/view')
        filters=list(view.findall('filter'))
        for f in filters:view.remove(f)
        insertion=1+list(view).index(view.findall('datasource-dependencies')[-1])
        for i,f in enumerate(filters):view.insert(insertion+i,f)
        seg=E.Element('filter',{'class':'categorical','column':'[analysis].[none:Segment:nk]'})
        union=E.SubElement(seg,'groupfilter',{'function':'union'})
        for segment, in db.execute('SELECT DISTINCT segment FROM bookings ORDER BY segment'):
            E.SubElement(union,'groupfilter',{'function':'member','level':'[none:Segment:nk]','member':json.dumps(segment)})
        view.insert(insertion+len(filters),seg)
    for parent in book.findall('.//zones/zone'):
        styles=list(parent.findall('zone-style'))
        for style in styles:parent.remove(style);parent.append(style)
    for group in list(book.findall('filter-group')):book.remove(group)
    for win in book.findall('./windows/window'):
        if win.get('class')=='worksheet' and win.find('cards') is None:win.insert(0,E.Element('cards'))
        if win.get('class')=='dashboard' and win.find('viewpoints') is None:win.insert(0,E.Element('viewpoints'))
    shared=E.Element('shared-views');sv=E.SubElement(shared,'shared-view',{'name':'analysis'})
    sv.append(copy.deepcopy(book.find('./worksheets/worksheet/table/view/datasources')))
    dep=E.SubElement(sv,'datasource-dependencies',{'datasource':'analysis'})
    first=book.find('./worksheets/worksheet/table/view')
    for field in ['Hotel','Year','Period','Segment']:
        E.SubElement(dep,'column',{'datatype':'string','name':f'[{field}]','role':'dimension','type':'nominal'})
        E.SubElement(dep,'column-instance',{'column':f'[{field}]','derivation':'None','name':f'[none:{field}:nk]','pivot':'key','type':'nominal'})
    for field in ['Hotel','Year','Period','Segment']:
        if field=='Period':
            f=E.Element('filter',{'class':'categorical','column':'[analysis].[none:Period:nk]'})
            union=E.SubElement(f,'groupfilter',{'function':'union'})
            for period, in db.execute('SELECT DISTINCT period FROM bookings ORDER BY period'):E.SubElement(union,'groupfilter',{'function':'member','level':'[none:Period:nk]','member':json.dumps(period)})
        else:f=copy.deepcopy(first.find(f'filter[@column="[analysis].[none:{field}:nk]"]'))
        sv.append(f)
        for sheet in book.findall('./worksheets/worksheet'):
            view=sheet.find('./table/view')
            for local in list(view.findall(f'filter[@column="[analysis].[none:{field}:nk]"]')):view.remove(local)
    book.insert(list(book).index(book.find('worksheets')),shared)
    # Larger bars first. Period remains in chronological order.
    for sort in book.findall('.//view/sort'):sort.set('direction','DESC')
    for sheet in book.findall('./worksheets/worksheet'):
        if sheet.get('name')=='Lead-time rate':
            for sort in list(sheet.findall('./table/view/sort')):sheet.find('./table/view').remove(sort)
        for mark in sheet.findall('./table/panes/pane/mark'):
            palette=E.SubElement(sheet.find('./table/panes/pane/style'),'style-rule',{'element':'mark'})
            E.SubElement(palette,'format',{'attr':'color','value':b.TEAL})
        color=sheet.find('./table/panes/pane/encodings/color')
        if color is not None:sheet.find('./table/panes/pane/encodings').remove(color)
    labelcol=ds.find('column[@name="[Label]"]');aliases=E.SubElement(labelcol,'aliases')
    from datetime import datetime
    for period, in db.execute('SELECT DISTINCT period FROM bookings ORDER BY period'):
        E.SubElement(aliases,'alias',{'key':json.dumps(period),'value':datetime.strptime(period,'%Y-%m').strftime('%y%m')})
    decision=book.find('./windows/window[@name="01  Decision brief"]');book.find('windows').remove(decision);book.find('windows').append(decision)
    E.indent(book);tree.write(path,encoding='utf-8',xml_declaration=True)
    # Reapply the source-controlled presentation after generation.
    import subprocess,sys
    subprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/"tools"/"apply_visual_theme.py")],check=True)
    print(path)

if __name__=='__main__':build()


