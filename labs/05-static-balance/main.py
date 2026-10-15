"""Convex support region and signed distance of a projected center of mass."""
import math,json
from pathlib import Path

def hull(points):
    pts=sorted(set(tuple(p) for p in points))
    if any(len(p)!=2 or not all(math.isfinite(v) for v in p) for p in pts):raise ValueError('Finite 2D points are required.')
    def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    if len(pts)<3:raise ValueError('At least three noncollinear points required.')
    lower=[];upper=[]
    for p in pts:
        while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0:lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0:upper.pop()
        upper.append(p)
    result=lower[:-1]+upper[:-1]
    if len(result)<3:raise ValueError('Contact region has zero area.')
    return result

def signed_margin(contact_points,com):
    polygon=hull(contact_points)
    if len(com)!=2 or not all(math.isfinite(v) for v in com):raise ValueError('Finite 2D COM projection required.')
    inside=True;distances=[]
    for a,b in zip(polygon,polygon[1:]+polygon[:1]):
        dx,dy=b[0]-a[0],b[1]-a[1]
        cross=dx*(com[1]-a[1])-dy*(com[0]-a[0])
        if cross < -1e-12:inside=False
        t=max(0.0,min(1.0,((com[0]-a[0])*dx+(com[1]-a[1])*dy)/(dx*dx+dy*dy)))
        q=(a[0]+t*dx,a[1]+t*dy)
        distances.append(math.hypot(com[0]-q[0],com[1]-q[1]))
    distance=min(distances)
    if distance<1e-12:return 0.0
    return distance if inside else -distance

def render_svg(polygon,com):
    def xy(p):return (300+p[0]*800,230-p[1]*800)
    line=' '.join(f'{x:.2f},{y:.2f}' for x,y in map(xy,polygon));x,y=xy(com)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="450" viewBox="0 0 600 450"><rect width="600" height="450" fill="#f4f7fa"/><text x="24" y="32" font-size="20">Quasi-static support region</text><polygon points="{line}" fill="#c8e2d3" stroke="#287b54" stroke-width="3"/><circle cx="{x}" cy="{y}" r="7" fill="#c34c3c"/><text x="24" y="415" font-size="14">Red: projected center of mass. No dynamic stability claim.</text></svg>'

if __name__=='__main__':
    contacts=[(-0.15,-0.10),(-0.15,0.10),(-0.05,-0.10),(-0.05,0.10),(0.05,-0.10),(0.05,0.10),(0.15,-0.10),(0.15,0.10)]
    com=(0.03,0.02);polygon=hull(contacts)
    out=Path('outputs');out.mkdir(exist_ok=True);(out/'support.svg').write_text(render_svg(polygon,com))
    print(json.dumps({'support_polygon_m':polygon,'com_projection_m':com,'signed_margin_m':signed_margin(contacts,com),'assumption':'fixed coplanar contacts, gravity only, adequate friction, quasi-static','svg':str(out/'support.svg')},indent=2))
