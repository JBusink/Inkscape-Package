"""Rebuild Libraries, Overviews and index.html from Components and catalog.json.
Python standard library only. No artwork generators run during this build.
"""
from pathlib import Path
from copy import deepcopy
import json,math,re,html,sys,xml.etree.ElementTree as ET
sys.dont_write_bytecode=True

P=Path(__file__).resolve().parent.parent
N='http://www.w3.org/2000/svg';XL='http://www.w3.org/1999/xlink'
ET.register_namespace('',N);ET.register_namespace('xlink',XL)
def tag(t):return '{'+N+'}'+t
def text(root,x,y,value,size=14,**extra):
 ET.SubElement(root,tag('text'),{'x':str(x),'y':str(y),'fill':'#30424b','font-family':'Arial, sans-serif','font-size':str(size),**extra}).text=value
def graphic(row,prefix):
 root=ET.parse(P/row['file']).getroot()
 assert not any(e.tag.rsplit('}',1)[-1] in ('text','tspan','flowRoot','foreignObject') for e in root.iter()),row['file']+' contains live text'
 ids={e.get('id'):prefix+'-'+e.get('id') for e in root.iter() if e.get('id')}
 for e in root.iter():
  for k,v in list(e.attrib.items()):
   if k=='id':e.set(k,ids[v]);continue
   v=re.sub(r'url\(#([^)]*)\)',lambda m:'url(#'+ids.get(m[1],m[1])+')',v)
   if k.endswith('href') and v.startswith('#'):v='#'+ids.get(v[1:],v[1:])
   e.set(k,v)
 g=ET.Element(tag('g'),{k:v for k,v in root.attrib.items() if k in ('style','fill','stroke','stroke-width','opacity','color','font-family')})
 for e in root:
  if e.tag.rsplit('}',1)[-1] not in ('title','desc','metadata','namedview'):g.append(deepcopy(e))
 vb=list(map(float,root.get('viewBox','0 0 200 150').replace(',',' ').split()))
 return g,vb
def validate(root):
 ids=[e.get('id') for e in root.iter() if e.get('id')];assert len(ids)==len(set(ids)),'Duplicate SVG IDs';known=set(ids)
 for e in root.iter():
  for k,v in e.attrib.items():
   refs=re.findall(r'url\(#([^)]*)\)',v)
   if k.endswith('href') and v.startswith('#'):refs.append(v[1:])
   assert all(r in known for r in refs),refs


def render_readme():
 from urllib.parse import urlsplit
 source=(P.parents[1]/'README.md').read_text(encoding='utf-8')
 def inline(value):
  tokens=[]
  def keep(markup):
   tokens.append(markup);return '\x00'+str(len(tokens)-1)+'\x00'
  def link(m):
   label,url=m.groups()
   parsed=urlsplit(url)
   if parsed.scheme and parsed.scheme not in ('http','https','mailto'):raise ValueError('Unsupported README link')
   if not parsed.scheme and not url.startswith('#'):url='../../'+url
   return keep('<a href="'+html.escape(url,quote=True)+'">'+html.escape(label)+'</a>')
  value=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,value)
  value=re.sub(r'`([^`]+)`',lambda m:keep('<code>'+html.escape(m[1])+'</code>'),value)
  value=html.escape(value)
  return re.sub(r'\x00(\d+)\x00',lambda m:tokens[int(m[1])],value)
 out=[];paragraph=[];listing=False;code=None
 def flush():
  if paragraph:out.append('<p>'+inline(' '.join(paragraph))+'</p>');paragraph.clear()
 for line in source.splitlines():
  if line.startswith('```'):
   flush()
   if listing:out.append('</ul>');listing=False
   if code is None:code=[]
   else:out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>');code=None
   continue
  if code is not None:code.append(line);continue
  if line.startswith('- '):
   flush()
   if not listing:out.append('<ul>');listing=True
   out.append('<li>'+inline(line[2:])+'</li>');continue
  if listing:out.append('</ul>');listing=False
  if line.startswith('#'):
   flush();level=min(len(line)-len(line.lstrip('#')),6)
   out.append(f'<h{level}>'+inline(line[level:].strip())+f'</h{level}>')
  elif line.strip():paragraph.append(line.strip())
  else:flush()
 flush()
 if listing:out.append('</ul>')
 if code is not None:raise ValueError('Unclosed README code block')
 return '\n'.join(out)

def build():
 data=json.loads((P/'Maintenance/catalog.json').read_text(encoding='utf-8'))
 assert all(r['category'] in {cat['id'] for cat in data['categories']} for r in data['components']), 'Unknown component category'
 assert len({r['id'] for r in data['components']})==len(data['components'])
 for folder in ('Libraries','Overviews'):(P/folder).mkdir(exist_ok=True)
 for cat in data['categories']:
  chosen=[r for r in data['components'] if r['category']==cat['id']]
  height=110+math.ceil(len(chosen)/4)*225
  lib=ET.Element(tag('svg'),{'width':'1200','height':str(height),'viewBox':f'0 0 1200 {height}'})
  ET.SubElement(lib,tag('title')).text=cat['name'];defs=ET.SubElement(lib,tag('defs'))
  sheet=ET.Element(tag('svg'),{'width':'297mm','height':str(height*297/1200)+'mm','viewBox':f'0 0 1200 {height}'})
  ET.SubElement(sheet,tag('rect'),{'width':'1200','height':str(height),'fill':'white'})
  text(sheet,34,47,cat['name'],28,**{'font-weight':'bold'});text(sheet,34,76,f'{len(chosen)} components',14)
  for i,row in enumerate(chosen):
   g,vb=graphic(row,row['id']);sym=ET.SubElement(defs,tag('symbol'),{'id':row['id']})
   ET.SubElement(sym,tag('title')).text=row['name']
   if row.get('credit'):ET.SubElement(sym,tag('desc')).text=row['credit']
   sym.append(g)
   x=22+(i%4)*295;y=96+(i//4)*225;scale=min(235/vb[2],145/vb[3]);dx=x+140-(vb[0]+vb[2]/2)*scale;dy=y+84-(vb[1]+vb[3]/2)*scale
   transform=f'translate({dx} {dy}) scale({scale})'
   ET.SubElement(lib,tag('use'),{'{'+XL+'}href':'#'+row['id'],'transform':transform})
   ET.SubElement(sheet,tag('rect'),{'x':str(x),'y':str(y),'width':'280','height':'210','rx':'8','fill':'#f6f8f9','stroke':'#dce4e7'})
   art,_=graphic(row,'sheet-'+row['id']);art.set('transform',transform);sheet.append(art)
   text(sheet,x+140,y+180,row['name'],12 if len(row['name'])>28 else 14,**{'text-anchor':'middle','font-weight':'bold'})
  for root in (lib,sheet):validate(root)
  ET.ElementTree(lib).write(P/cat['library'],encoding='utf-8',xml_declaration=True)
  ET.ElementTree(sheet).write(P/cat['overview'],encoding='utf-8',xml_declaration=True)
 # Examples are standalone authored SVGs; preserve them during rebuilds.
 for row in data['components']+data['examples']:assert (P/row['file']).is_file(),row['file']
 encoded=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
 (P/'index.html').write_text(PAGE.replace('__CATALOG__',encoded).replace('__README__',render_readme()),encoding='utf-8')
 print(f"Built {len(data['components'])} components, {len(data['categories'])} libraries, {len(data['examples'])} examples. Open index.html.")

PAGE='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Science symbols</title>
<style>
:root{font-family:Segoe UI,Arial,sans-serif;color:#253943;background:#f6f8f9;font-size:15px}*{box-sizing:border-box}body{margin:0}a{color:inherit}button,input{font:inherit}button,a,input{outline-offset:4px}button{cursor:pointer}header{height:76px;display:flex;align-items:center;gap:24px;padding:0 28px;border-bottom:1px solid #dce4e8;background:white;position:sticky;top:0;z-index:2}.brand{font-size:22px;font-weight:650;text-decoration:none;white-space:nowrap}.brand span{color:#598494;margin-right:10px}header input{flex:1;min-width:140px;max-width:650px;padding:12px 15px;border:1px solid #cbd7dd;border-radius:8px;background:#f7f9fa}.modes{display:flex;gap:5px;margin-left:auto}.modes button{padding:10px 16px;border:0;border-radius:7px;background:transparent;color:#4c626d}.modes button[aria-pressed=true]{background:#294957;color:white}.layout{display:grid;grid-template-columns:205px 1fr;max-width:1800px;margin:auto}aside{position:sticky;top:76px;height:calc(100vh - 76px);overflow:auto;padding:22px 14px}nav{display:grid;gap:3px}nav button{display:flex;align-items:center;justify-content:space-between;text-align:left;padding:10px 12px;border:0;border-radius:7px;background:transparent;color:#425b67}nav button:hover{background:#e9eff2}nav button[aria-current=true]{background:#dce8ed;color:#223e4a;font-weight:650}nav small{font-size:11px;opacity:.7}main{min-width:0;padding:28px 28px 30px 16px}.toolbar{display:flex;align-items:center;flex-wrap:wrap;gap:12px;margin-bottom:22px}h1{font-size:25px;font-weight:600;margin:0}#count{font-size:13px;color:#6d8089}.downloads{margin-left:auto;display:flex;gap:8px}.downloads a{padding:9px 12px;border:1px solid #c8d5db;border-radius:7px;text-decoration:none;background:white;font-size:13px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(205px,1fr));gap:15px}.grid.examples{grid-template-columns:repeat(auto-fill,minmax(340px,1fr))}.card{background:white;border:1px solid #dde5e9;border-radius:9px;overflow:hidden}.art{display:flex;align-items:center;justify-content:center;background:#fdfefe;height:168px;padding:15px}.art img{width:100%;height:100%;object-fit:contain}.examples .art{height:auto;aspect-ratio:1.6;padding:8px}.card:hover{border-color:#8aa8b5;box-shadow:0 3px 14px #263e4b0c}.card footer{padding:13px 14px;display:flex;align-items:center;gap:8px;border-top:1px solid #eef2f4}.card h2{font-size:13px;line-height:1.4;font-weight:600;margin:0;flex:1}.save{font-size:12px;color:#44778a;text-decoration:none;white-space:nowrap}#more{display:block;margin:24px auto;padding:10px 28px;background:white;border:1px solid #c7d5dc;border-radius:7px;color:#385969}[hidden]{display:none!important}.empty{padding:40px 0;color:#657b86}.credit{font-size:11px;color:#71838b;line-height:1.6;margin:32px 0 0}.credit a{color:inherit}#top{color:#697f8a;font-size:12px;text-decoration:none;display:block;text-align:right;margin-top:22px}@media(max-width:760px){header{height:auto;flex-wrap:wrap;padding:14px;gap:12px}.brand{font-size:20px}header input{order:3;max-width:none;width:100%}.modes{margin-left:auto}.modes button{padding:8px 10px}.layout{grid-template-columns:1fr}aside{position:static;height:auto;padding:12px}nav{display:flex;overflow:auto;gap:6px}nav button{white-space:nowrap;gap:12px;background:#eaf0f3}main{padding:10px 14px 24px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.grid.examples{grid-template-columns:1fr}.art{height:140px}.downloads{margin-left:0}.toolbar{gap:9px}}@media(prefers-reduced-motion:no-preference){.card{transition:border-color .15s}}
dialog{max-width:780px;width:calc(100% - 48px);max-height:85vh;border:1px solid #bdcdd4;border-radius:12px;padding:24px;color:#253943}dialog::backdrop{background:#172c3b70}.readme-body{line-height:1.6}.readme-body h1{margin:10px 0}.readme-body h2{margin-top:26px;font-size:20px}.readme-body pre{overflow:auto;background:#eef3f4;padding:12px;border-radius:6px}.readme-body code{font-size:.9em}.readme-body a{color:#326d83}dialog form{text-align:right}dialog button{padding:8px 14px;border:1px solid #bdcdd4;background:white;border-radius:5px}</style></head><body>
<header><a class="brand" href="#"><span>Φ</span>Science symbols</a><input id="search" type="search" placeholder="Search components…" aria-label="Search library" autocomplete="off"><div class="modes"><button id="components" aria-pressed="true">Components</button><button id="examples" aria-pressed="false">Examples</button><button id="readme-open" aria-haspopup="dialog">README</button></div></header>
<div class="layout"><aside><nav id="categories" aria-label="Categories"></nav></aside><main><div class="toolbar"><h1 id="title">Components</h1><span id="count" aria-live="polite"></span><div id="downloads" class="downloads"></div></div><div id="grid" class="grid"></div><p id="empty" class="empty" hidden>No matches.</p><button id="more" hidden>Show more</button><a id="top" href="#">↑ Top</a></main></div>
<dialog id="readme-dialog" aria-label="Science symbols README"><form method="dialog"><button autofocus>Close</button></form><article class="readme-body">__README__</article><p><a href="../../README.md" download>Download README.md</a></p></dialog>
<script id="catalog" type="application/json">__CATALOG__</script>
<script>
'use strict';const data=JSON.parse(document.getElementById('catalog').textContent),$=id=>document.getElementById(id);let mode='components',category='',limit=60;
const clean=s=>s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();
$('readme-open').onclick=()=>$('readme-dialog').showModal();
function readHash(){const p=new URLSearchParams(location.hash.slice(1));mode=p.get('mode')==='examples'?'examples':'components';category=p.get('category')||'';if(mode==='examples'||!data.categories.some(c=>c.id===category))category='';$('search').value=p.get('q')||'';limit=60;render()}
function url(){const p=new URLSearchParams;if(mode==='examples')p.set('mode',mode);if(category)p.set('category',category);if($('search').value)p.set('q',$('search').value);history.replaceState(null,'',location.pathname+(p.size?'#'+p.toString():''))}
function choose(c){category=c;limit=60;url();render();window.scrollTo(0,0)}
function download(parent,name,file){const a=document.createElement('a');a.textContent=name;a.href=file;a.download='';parent.append(a)}
function render(){
 $('components').setAttribute('aria-pressed',mode==='components');$('examples').setAttribute('aria-pressed',mode==='examples');$('search').placeholder=mode==='components'?'Search components…':'Search examples…';
 document.querySelector('aside').hidden=mode==='examples';document.querySelector('.layout').style.gridTemplateColumns=mode==='examples'?'1fr':'';const cats=mode==='examples'?[]:[{id:'',name:'All'},...data.categories];$('categories').replaceChildren();for(const c of cats){const n=data[mode].filter(r=>!c.id||r.category===c.id||(r.categories||[]).includes(c.id)).length;if(mode==='examples'&&!n)continue;const b=document.createElement('button');b.textContent=c.name;b.setAttribute('aria-current',category===c.id);const span=document.createElement('small');span.textContent=n;b.append(span);b.onclick=()=>choose(c.id);$('categories').append(b)}
 const cat=data.categories.find(c=>c.id===category);$('title').textContent=(cat?cat.name+' · ':'')+(mode==='examples'?'Examples':'Components');$('downloads').replaceChildren();if(cat&&mode==='components'){download($('downloads'),'Inkscape library ↓',cat.library);download($('downloads'),'Overview ↓',cat.overview)}
 const terms=clean($('search').value).trim().split(/\\s+/).filter(Boolean);const rows=data[mode].filter(r=>(!category||r.category===category||(r.categories||[]).includes(category))&&terms.every(q=>clean(r.name+' '+(r.group||'')+' '+(r.keywords||'')+' '+(r.category||'')).includes(q)));
 $('count').textContent=rows.length+' items';$('grid').className='grid'+(mode==='examples'?' examples':'');$('grid').replaceChildren();const frag=document.createDocumentFragment();for(const r of rows.slice(0,limit)){const card=document.createElement('article');card.className='card';const a=document.createElement('a');a.className='art';a.href=r.file;a.target='_blank';a.rel='noopener';a.title=r.name;const img=document.createElement('img');img.src=r.file;img.alt=r.name;img.loading='lazy';img.decoding='async';a.append(img);const f=document.createElement('footer');const name=document.createElement('h2');name.textContent=r.name;f.append(name);const save=document.createElement('a');save.className='save';save.href=r.file;save.download='';save.textContent='SVG ↓';save.setAttribute('aria-label','Download '+r.name);f.append(save);card.append(a,f);frag.append(card)}$('grid').append(frag);$('empty').hidden=rows.length>0;$('more').hidden=rows.length<=limit;
}
for(const m of ['components','examples'])$(m).onclick=()=>{mode=m;category='';limit=60;$('search').value='';url();render();window.scrollTo(0,0)};
$('search').oninput=()=>{limit=60;url();render()};$('more').onclick=()=>{limit+=60;render()};$('top').onclick=e=>{e.preventDefault();window.scrollTo(0,0)};window.addEventListener('hashchange',readHash);readHash();
</script></body></html>'''
if __name__=='__main__':build()
