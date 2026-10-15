"""Validate the learning catalog and six original teaching labs."""
from pathlib import Path
import json, importlib.util, xml.etree.ElementTree as ET
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
def load(path):
    spec=importlib.util.spec_from_file_location(path.replace('/','_'),ROOT/path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
catalog=json.loads((ROOT/'catalog.json').read_text())['categories']
assert len(catalog)==60
assert len({c['track'] for c in catalog})==8
assert sum(c['track']=='Humanoid Robotics' for c in catalog)==12
assert len({c['slug'] for c in catalog})==len(catalog)
for c in catalog:
    assert (ROOT/'categories'/f"{c['slug']}.md").is_file()
    for r in c['resources']: assert urlparse(r['url']).scheme=='https'
panel=load('labs/01-panel-geometry/main.py')
svg=ET.fromstring(panel.panel_svg(180,120,'P001'))
assert svg.attrib['width']=='180mm' and svg.attrib['height']=='120mm'
assert svg.find('{http://www.w3.org/2000/svg}path').attrib['d'].endswith('Z')
try: panel.panel_svg(-1,120)
except ValueError: pass
else: raise AssertionError('Invalid panel accepted')
fit=load('labs/02-fit-predictor/main.py')
assert fit.predict_fit(2.9,3.0,0.2)['prediction']=='within_assumed_clearance_range'
assert fit.predict_fit(2.7,3.0,0.2)['prediction']=='outside_assumed_clearance_range'
assert fit.predict_fit(2.85,3.0,0.2,0.03,0.02)['prediction']=='uncertain'
assert fit.predict_fit(2.9,3.0,0.2,0.03,0.02)['prediction']=='within_assumed_clearance_range'
packing=load('labs/03-sheet-packing/main.py')
parts=[{'id':f'P{i}','w':50,'h':h} for i,h in enumerate([70,20,70,20])]
assert packing.pack(parts)['sheets']==2
result=packing.pack(sorted(parts,key=lambda p:-p['h']))
assert result['sheets']==1 and result['utilization']==0.9
assert packing.pack([])['sheets']==0
for p in result['placements']:
    assert 0<=p['x'] and p['x']+p['w']<=100 and 0<=p['y'] and p['y']+p['h']<=100
for i,a in enumerate(result['placements']):
    for b in result['placements'][i+1:]:
        if a['sheet']==b['sheet']:
            assert a['x']+a['w']<=b['x'] or b['x']+b['w']<=a['x'] or a['y']+a['h']<=b['y'] or b['y']+b['h']<=a['y']
try: packing.pack([{'id':'too-big','w':101,'h':20}])
except ValueError: pass
else: raise AssertionError('Oversize part accepted')
limb=load('labs/04-limb-kinematics/main.py')
import math
assert limb.forward([1,1],[0,0])[-1]==(2.0,0.0)
folded=limb.forward([1,1],[0,math.pi])[-1]
assert math.hypot(*folded)<1e-12
for lengths,angles in [([0.35,0.30,0.12],[0.7,-1.1,0.5]),([1,1],[0,0]),([1,1],[0,math.pi])]:
    assert limb.finite_difference_error(lengths,angles)<1e-7
ET.fromstring(limb.render_svg(limb.forward([0.3,0.2],[0.5,0.5])))
balance=load('labs/05-static-balance/main.py')
square=[(-1,-1),(1,-1),(1,1),(-1,1)]
assert balance.hull(square+[(0,0),square[0]])==balance.hull(square)
assert math.isclose(balance.signed_margin(square,(0,0)),1.0)
assert balance.signed_margin(square,(1,0))==0
assert math.isclose(balance.signed_margin(square,(2,0)),-1.0)
assert math.isclose(balance.signed_margin(square,(2,2)),-math.sqrt(2))
ET.fromstring(balance.render_svg(balance.hull(square),(0,0)))
supervision=load('labs/06-human-supervision/main.py')
def rejects(action):
    try:action()
    except ValueError:return
    raise AssertionError('Invalid operation was accepted')
rejects(lambda:limb.forward([0],[0]))
rejects(lambda:limb.forward([1,1],[0]))
rejects(lambda:balance.hull([(0,0),(1,0),(2,0)]))
s=supervision.Supervisor()
rejects(s.start);rejects(s.approve)
s.stop();s.stop();rejects(s.start);rejects(lambda:s.propose('Task A'))
s.reset();s.propose('Task A');s.approve()
rejects(lambda:s.propose('Changed task'))
s.start();s.stop();rejects(s.start)
s.reset();assert s.task is None
rejects(s.start);s.propose('Task B');rejects(s.start)
s.approve();s.start();s.complete();assert s.state==supervision.State.IDLE and s.task is None
assert s.events[-1]['event']=='complete' and s.events[-1]['state']=='idle'
import re
for doc in ROOT.rglob('*.md'):
    if 'external' in doc.relative_to(ROOT).parts:continue
    for target in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
        if '://' not in target and not target.startswith('#'):
            assert (doc.parent/target).exists(),(str(doc),target)
print('PASS: 60 categories, 8 tracks, 12 humanoid topics, local links, and six labs including numerical and failure-case checks.')
