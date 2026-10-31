"""Download only the documented pinned Kaggle source; no credentials are stored."""
from pathlib import Path
import urllib.request,zipfile,io,json,hashlib
P=Path(__file__).resolve().parents[1]
meta=json.loads((P/'data/source-download.json').read_text())
b=urllib.request.urlopen(meta['url'],timeout=90).read()
with zipfile.ZipFile(io.BytesIO(b)) as z:
 for f in meta['files']:
  n=next(n for n in z.namelist() if Path(n).name==f['name'])
  data=z.read(n)
  if hashlib.sha256(data).hexdigest()!=f['sha256']:raise ValueError('Kaggle content changed; review source version before replacing data')
  path=P/'data/raw'/f['name'];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
print('Pinned source downloaded and verified')
