"""Apply this project's native presentation tokens without changing data logic."""
from pathlib import Path
import copy,hashlib,json,re,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1]
TOKEN_PATH=ROOT/'design-tokens.json'

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def semantic_json(data):
    # All query projections, filters, interactions and textual values are retained.
    if isinstance(data,list):return [semantic_json(x) for x in data]
    if not isinstance(data,dict):return data
    return {k:semantic_json(v) for k,v in data.items() if k not in {
        'visualContainerObjects','textStyle','themeCollection','resourcePackages',
        'categoryAxis','valueAxis','legend','labels','categoryLabels','dataPoint',
        'columnHeaders','values','grid','background','border','title','style','styles',
        'outspace','filterCard','pageInformation','color','fontColor',
        'backColor','fontColorPrimary','backColorPrimary'}}

def native_semantics(book):
    b=copy.deepcopy(book)
    for parent in list(b.iter()):
        for child in list(parent):
            if child.tag in {'style','style-theme','zone-style','layout-options'}:
                parent.remove(child)
    for e in b.iter():
        if e.tag=='zone':
            for key in ['x','y','w','h']:e.attrib.pop(key,None)
        for key in list(e.attrib):
            if key in {'fontcolor','fontname','fontsize','bold','italic','color'}:
                del e.attrib[key]
    return E.tostring(b)

def apply(root=ROOT,tableau_path=None):
    root=Path(root);t=json.loads((root/'design-tokens.json').read_text())
    c=t['colors']; aliases={k.upper():c[v] for k,v in t['native_aliases'].items()}
    def recolor(value):
        if isinstance(value,str):return re.sub(r'#[0-9a-fA-F]{6}',lambda m:aliases.get(m[0].upper(),m[0]),value)
        if isinstance(value,list):return [recolor(x) for x in value]
        if isinstance(value,dict):return {k:recolor(v) for k,v in value.items()}
        return value
    records=[]
    for report in root.rglob('*.Report'):
        for p in list((report/'definition').rglob('*.json'))+list((report/'StaticResources/RegisteredResources').glob('*')):
            if not p.is_file():continue
            try:a=json.loads(p.read_text(encoding='utf-8-sig'))
            except (ValueError,UnicodeError):continue
            old=digest(semantic_json(a));b=recolor(a)
            # Native theme's defaults also cover new visuals added interactively.
            if p.parent.name=='RegisteredResources':
                b.update(name=t['name'],dataColors=[c['primary'],c['accent'],c['prior']],
                    background=c['canvas'],foreground=c['ink'],tableAccent=c['primary'])
                b['textClasses']={role:{'fontFace':'Segoe UI','color':c['ink'] if role!='label' else c['muted']} for role in ['title','header','label','callout']}
            else:assert digest(semantic_json(b))==old,str(p)
            if a!=b:p.write_text(json.dumps(b,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
            if p.name in {'visual.json','page.json'}:records.append({'file':p.relative_to(root).as_posix(),'semantic_sha256':old})
    paths=[Path(tableau_path)] if tableau_path else list((root/'tableau').glob('*.twb'))
    for p in paths:
        tree=E.parse(p);book=tree.getroot();before=hashlib.sha256(native_semantics(book)).hexdigest()
        for element in book.iter():
            for attr,value in list(element.attrib.items()):
                if attr in {'fontcolor','value','to','color'}:
                    element.set(attr,recolor(value))
                if attr=='fontname' and value in {'Georgia','Calibri'}:element.set(attr,'Segoe UI')
        for encoding in book.findall('.//encoding'):
            if encoding.get('attr')!='color':continue
            for mapping in encoding.findall('map'):
                try:member=json.loads(mapping.findtext('bucket'))
                except (ValueError,TypeError):continue
                if member in {'Partial final month','Higher reported net'}:mapping.set('to','#996A13')
        if root.name=='retail-sales-data-quality':
            zones={z.get('id'):z for z in book.findall('./dashboards/dashboard/zones/zone/zone')}
            for ids,bg,ink in [(['5','6','7'],'#EEEDFC',c['primary']),(['8','9','10'],'#F1F2F8',c['ink']),(['11','12','13'],'#FAEDF5',c['accent'])]:
                for key in ids:
                    z=zones.get(key)
                    if z is None:continue
                    style=z.find('zone-style')
                    if style is None:style=E.SubElement(z,'zone-style')
                    setting=next((f for f in style.findall('format') if f.get('attr')=='background-color'),None)
                    if setting is None:setting=E.SubElement(style,'format',attr='background-color')
                    setting.set('value',bg)
                    if key==ids[1]:
                        for run in z.findall('formatted-text/run'):run.set('fontcolor',ink);run.set('fontsize','34')
        if root.name=='hotel-booking-cancellation-analysis':
            # mark-color is Tableau's native mark fill; color controls text.
            for sheet in book.findall('./worksheets/worksheet'):
                name=sheet.get('name')
                ink=c['accent'] if name in {'Segment rate','Selected rate','Selected cancellations'} else c['primary']
                styles=sheet.findall('./table/panes/pane/style')
                for style in styles:
                    for old in style.findall('./style-rule[@element="mark"]/format[@attr="mark-color"]'):
                        for rule in style: 
                            if old in list(rule):rule.remove(old)
                    rule=E.SubElement(style,'style-rule',element='mark')
                    E.SubElement(rule,'format',attr='mark-color',value=ink)
                    if name in {'Selected bookings','Selected cancellations','Selected rate','Canceled booked nights'}:
                        E.SubElement(rule,'format',attr='color',value=ink)
                        E.SubElement(rule,'format',attr='font-size',value='26')
            def zone_style(zone,bg):
                style=zone.find('zone-style')
                if style is None:style=E.SubElement(zone,'zone-style')
                for attr,value in [('background-color',bg),('padding','18')]:
                    setting=next((f for f in style.findall('format') if f.get('attr')==attr),None)
                    if setting is None:setting=E.SubElement(style,'format',attr=attr)
                    setting.set('value',value)
            for dashboard in book.findall('./dashboards/dashboard'):
                if dashboard.get('name')=='01  Decision brief':
                    for zone in dashboard.findall('./zones/zone/zone'):
                        if zone.get('id') in {'100','101','102','103'}:
                            zone_style(zone,c['soft'] if zone.get('id') in {'101','102'} else '#EDF2FC')
                            zone.set('h','11000')
                            for setting in zone.findall('zone-style/format'):
                                if setting.get('attr')=='padding':setting.set('value','6')
                if dashboard.get('name')=='02  Definitions and trial':
                    for zone in dashboard.findall('./zones/zone/zone'):
                        key=zone.get('id')
                        layouts={'200':(32,26,1336,80,30),'201':(32,106,1336,130,14),'202':(32,290,640,60,20),'203':(32,350,640,260,14),'204':(704,290,664,60,20),'205':(704,350,664,260,14)}
                        if key not in layouts:continue
                        x,y,w,h,size=layouts[key]
                        for attr,value,dimension in [('x',x,1400),('y',y,950),('w',w,1400),('h',h,950)]:zone.set(attr,str(round(value/dimension*100000)))
                        zone_style(zone,c['canvas'] if key in {'200','201'} else c['soft'] if key in {'204','205'} else '#EDF2FC')
                        for run in zone.findall('formatted-text/run'):
                            run.set('fontname','Segoe UI');run.set('fontsize',str(size));run.set('fontcolor',c['accent'] if key=='204' else c['ink']);run.set('bold','true' if key in {'200','202','204'} else 'false')
        assert hashlib.sha256(native_semantics(book)).hexdigest()==before,str(p)
        tree.write(p,encoding='utf-8',xml_declaration=True)
        records.append({'file':p.relative_to(root).as_posix(),'semantic_sha256':before})
    return records

if __name__=='__main__':
    print(json.dumps({'project':ROOT.name,'checked_native_objects':len(apply())}))
