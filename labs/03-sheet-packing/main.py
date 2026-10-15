"""Compare two orderings under a simple sequential shelf-packing heuristic."""
import json
import math

def pack(parts, bed=(100,100)):
    bw,bh=bed
    if not all(math.isfinite(v) and v>0 for v in bed): raise ValueError('Invalid bed dimensions.')
    if not parts: return {'sheets':0,'utilization':0.0,'placements':[]}
    if len({p['id'] for p in parts})!=len(parts): raise ValueError('Part IDs must be unique.')
    x=y=row_h=0; sheet=1; placements=[]
    for p in parts:
        w,h=p['w'],p['h']
        if not all(math.isfinite(v) and v>0 for v in (w,h)) or w>bw or h>bh:
            raise ValueError(f"Part {p['id']} cannot fit the bed without rotation.")
        if x+w>bw: y+=row_h; x=0; row_h=0
        if y+max(row_h,h)>bh: sheet+=1; x=y=row_h=0
        placements.append({'id':p['id'],'sheet':sheet,'x':x,'y':y,'w':w,'h':h})
        x+=w; row_h=max(row_h,h)
    return {'sheets':sheet,'utilization':sum(p['w']*p['h'] for p in parts)/(sheet*bw*bh),'placements':placements}

if __name__=='__main__':
    parts=[{'id':f'P{i+1}','w':50,'h':h} for i,h in enumerate([70,20,70,20])]
    baseline=pack(parts)
    candidate=pack(sorted(parts,key=lambda p:(-p['h'],p['id'])))
    print(json.dumps({'sample':'synthetic rectangles','baseline':baseline,'height_sorted':candidate,
        'sheets_saved':baseline['sheets']-candidate['sheets']},indent=2))
