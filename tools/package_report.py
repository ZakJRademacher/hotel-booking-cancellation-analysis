"""Package the native-saved Tableau source with relative data and attribution."""
from pathlib import Path
import zipfile,xml.etree.ElementTree as E
P=Path(__file__).resolve().parents[1]
source=P/'tableau/Hotel Cancellation Review.twb'
tree=E.parse(source)
for c in tree.findall('.//connection'):
    if c.get('class')=='textscan':c.set('directory','Data')
out=P/'deliverables/Hotel Cancellation Review.twbx';out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    z.writestr(source.name,E.tostring(tree.getroot(),encoding='utf-8',xml_declaration=True))
    for rel,arc in [('tableau/Data/analysis.csv','Data/analysis.csv'),('docs/SOURCES.md','docs/SOURCES.md'),('docs/METHOD.md','docs/METHOD.md'),('data/processed/controls.json','controls.json')]:z.write(P/rel,arc)
print(out)
