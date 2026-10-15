"""Planar limb forward kinematics and analytic endpoint Jacobian. Units: meters/radians."""
import math,json
from pathlib import Path

def forward(lengths,angles):
    if not lengths or len(lengths)!=len(angles):raise ValueError('One angle per positive link is required.')
    if not all(math.isfinite(v) and v>0 for v in lengths):raise ValueError('Invalid link length.')
    if not all(math.isfinite(v) for v in angles):raise ValueError('Invalid angle.')
    points=[(0.0,0.0)];theta=0.0
    for length,angle in zip(lengths,angles):
        theta+=angle
        x,y=points[-1]
        points.append((x+length*math.cos(theta),y+length*math.sin(theta)))
    return points

def jacobian(lengths,angles):
    points=forward(lengths,angles)
    ex,ey=points[-1]
    return [[-(ey-y),ex-x] for x,y in points[:-1]]

def finite_difference_error(lengths,angles,step=1e-6):
    if not math.isfinite(step) or step<=0:raise ValueError('Step must be positive.')
    analytical=jacobian(lengths,angles);errors=[]
    for i in range(len(angles)):
        plus=list(angles);minus=list(angles);plus[i]+=step;minus[i]-=step
        a=forward(lengths,plus)[-1];b=forward(lengths,minus)[-1]
        errors.extend(abs(analytical[i][j]-(a[j]-b[j])/(2*step)) for j in range(2))
    return max(errors)

def render_svg(points):
    scale=260;cx=210;cy=260
    xy=[(cx+x*scale,cy-y*scale) for x,y in points]
    line=' '.join(f'{x:.3f},{y:.3f}' for x,y in xy)
    return '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="450" viewBox="0 0 600 450"><rect width="600" height="450" fill="#f4f7fa"/><text x="24" y="32" font-size="20">Planar limb: forward kinematics</text><polyline points="'+line+'" fill="none" stroke="#2459ae" stroke-width="12" stroke-linecap="round"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="#db7b29"/><text x="{x+10}" y="{y+18}" font-size="15">J{i}</text>' for i,(x,y) in enumerate(xy))+'<text x="24" y="420" font-size="14">Illustrative geometry; meters converted to display pixels.</text></svg>'

if __name__=='__main__':
    lengths=[0.35,0.30,0.12];angles=[math.radians(v) for v in [40,-65,30]]
    points=forward(lengths,angles)
    error=finite_difference_error(lengths,angles)
    out=Path('outputs');out.mkdir(exist_ok=True)
    (out/'limb.svg').write_text(render_svg(points))
    print(json.dumps({'units':'meters, radians','joints':points,'endpoint_jacobian_columns':jacobian(lengths,angles),'max_finite_difference_error':error,'svg':str(out/'limb.svg')},indent=2))
