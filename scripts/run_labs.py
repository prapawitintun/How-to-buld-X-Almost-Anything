"""Run seven local lessons and the validator, preserving reproducible text outputs."""
from pathlib import Path
import subprocess,sys,json,platform
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]
LABS=['01-panel-geometry','02-fit-predictor','03-sheet-packing','04-limb-kinematics','05-static-balance','06-human-supervision','07-cad-to-robotics']
if __name__=='__main__':
    destination=ROOT/'examples/results';destination.mkdir(parents=True,exist_ok=True)
    results=[]
    for name in LABS:
        relative=f'labs/{name}/main.py'
        p=subprocess.run([sys.executable,relative],cwd=ROOT,capture_output=True,text=True)
        (destination/f'{name}.txt').write_text(p.stdout+p.stderr)
        results.append({'script':relative,'exit_code':p.returncode,'log':f'examples/results/{name}.txt'})
    p=subprocess.run([sys.executable,'scripts/validate.py'],cwd=ROOT,capture_output=True,text=True)
    (destination/'validation.txt').write_text(p.stdout+p.stderr)
    results.append({'script':'scripts/validate.py','exit_code':p.returncode,'log':'examples/results/validation.txt'})
    report={'executed_at':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'results':results,'scope':'Local educational calculations and software states only; no external robot framework or physical hardware evaluated.'}
    (ROOT/'validation-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'runs':len(results),'passed':sum(r['exit_code']==0 for r in results)},indent=2))
    if any(r['exit_code']!=0 for r in results):raise SystemExit(1)
