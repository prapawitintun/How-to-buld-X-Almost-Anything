"""CAD panels -> abstract sheet layout -> reachable planar-arm pick targets.

Teaching calculations only: no robot interface, gripper, collision model, or toolpath.
"""
from pathlib import Path
import importlib.util,json,math,heapq

ROOT=Path(__file__).resolve().parents[2]
def module(path):
    spec=importlib.util.spec_from_file_location(path.replace('/','_'),ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

packing=module('labs/03-sheet-packing/main.py')
limb=module('labs/04-limb-kinematics/main.py')

def inverse_2r(target,lengths=(0.4,0.3)):
    if len(target)!=2 or len(lengths)!=2:raise ValueError('Two-dimensional target and two link lengths required.')
    x,y=target;a,b=lengths
    if not all(math.isfinite(v) for v in (x,y,a,b)) or min(a,b)<=0:raise ValueError('Finite inputs and positive lengths required.')
    cosine=(x*x+y*y-a*a-b*b)/(2*a*b)
    if cosine < -1-1e-12 or cosine > 1+1e-12:raise ValueError('Target is unreachable.')
    q2=math.acos(max(-1.0,min(1.0,cosine)))
    q1=math.atan2(y,x)-math.atan2(b*math.sin(q2),a+b*math.cos(q2))
    return (q1,q2)

def dependency_order(requirements):
    if any(parent not in requirements for parents in requirements.values() for parent in parents):raise ValueError('Unknown predecessor.')
    remaining={name:set(parents) for name,parents in requirements.items()};ready=[name for name,parents in remaining.items() if not parents]
    heapq.heapify(ready);result=[]
    while ready:
        name=heapq.heappop(ready);result.append(name);remaining.pop(name)
        for other,parents in remaining.items():
            if name in parents:
                parents.remove(name)
                if not parents:heapq.heappush(ready,other)
    if remaining:raise ValueError('Dependency cycle.')
    return result

def build_demo(parts=None,requirements=None):
    if parts is None:parts=[{'id':f'P{i+1}','w':50,'h':h} for i,h in enumerate([70,20,70,20])]
    if requirements is None:requirements={'P1':[],'P2':['P1'],'P3':['P1'],'P4':['P2','P3']}
    if {p['id'] for p in parts}!=set(requirements):raise ValueError('Part IDs must match dependency IDs.')
    baseline=packing.pack(parts)
    candidate=packing.pack(sorted(parts,key=lambda p:(-p['h'],p['id'])))
    placements={p['id']:p for p in candidate['placements']};targets=[]
    for part_id in dependency_order(requirements):
        p=placements[part_id]
        # A 100 mm sheet is represented in a fixed robot XY frame.
        # Additional sheets are staged at +0.15 m increments along X.
        target=(0.35+(p['sheet']-1)*0.15+(p['x']+p['w']/2)/1000,-0.05+(p['y']+p['h']/2)/1000)
        angles=inverse_2r(target);actual=limb.forward([0.4,0.3],angles)[-1]
        error=math.dist(target,actual)
        targets.append({'part_id':part_id,'sheet':p['sheet'],'target_m':target,'joint_angles_rad':angles,'fk_error_m':error})
    return {'scope':'Synthetic 2D layout and kinematics; no collision-free or physical execution claim.',
        'units':{'panels':'mm','robot':'m','angles':'rad'},'parts':parts,'dependencies':requirements,
        'baseline':baseline,'candidate':candidate,'pick_sequence':targets,
        'max_fk_error_m':max((t['fk_error_m'] for t in targets),default=0)}

if __name__=='__main__':
    result=build_demo();out=ROOT/'outputs';out.mkdir(exist_ok=True)
    (out/'cad-to-robotics.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'output':'outputs/cad-to-robotics.json','baseline_sheets':result['baseline']['sheets'],
        'candidate_sheets':result['candidate']['sheets'],'pick_order':[t['part_id'] for t in result['pick_sequence']],
        'max_fk_error_m':result['max_fk_error_m'],'scope':result['scope']},indent=2))
