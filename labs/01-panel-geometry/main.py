"""Create a closed, numbered panel in millimeters. No CAD package required."""
from pathlib import Path
import argparse
import math

def panel_svg(width=180.0, height=120.0, part_id='P001'):
    if not all(math.isfinite(v) and v > 0 for v in (width, height)):
        raise ValueError('Panel dimensions must be finite and positive.')
    if not part_id.isalnum():
        raise ValueError('Part ID must contain only letters and numbers.')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}mm" height="{height}mm" viewBox="0 0 {width} {height}">
<title>{part_id}: {width} x {height} mm panel</title>
<path id="cut-{part_id}" d="M 0 0 L {width} 0 L {width} {height} L 0 {height} Z" fill="none" stroke="red" stroke-width="0.1"/>
<text x="{width/2}" y="{height/2}" text-anchor="middle" font-size="5" fill="black">{part_id}</text>
</svg>'''

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--width',type=float,default=180)
    p.add_argument('--height',type=float,default=120)
    p.add_argument('--id',default='P001')
    args=p.parse_args()
    target=Path('outputs/panel.svg'); target.parent.mkdir(exist_ok=True)
    target.write_text(panel_svg(args.width,args.height,args.id))
    print(f'Created {target}: {args.width} x {args.height} mm; closed boundary, one part ID.')
