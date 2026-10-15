"""Fetch an attributed, pinned upstream checkout without executing its code."""
from pathlib import Path
import json,subprocess

ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    m=json.loads((ROOT/'upstream/manifest.json').read_text())
    destination=ROOT/'external/build-your-own-x'
    if destination.exists(): raise SystemExit('Destination already exists; leaving it unchanged.')
    destination.parent.mkdir(exist_ok=True)
    subprocess.run(['git','init',str(destination)],check=True)
    subprocess.run(['git','-C',str(destination),'remote','add','origin',m['url']+'.git'],check=True)
    subprocess.run(['git','-C',str(destination),'fetch','--depth','1','origin',m['commit']],check=True)
    subprocess.run(['git','-C',str(destination),'checkout','--detach','FETCH_HEAD'],check=True)
    actual=subprocess.check_output(['git','-C',str(destination),'rev-parse','HEAD'],text=True).strip()
    if actual!=m['commit']:raise SystemExit('Commit verification failed.')
    print('Verified upstream checkout:',actual)
    print('Read upstream/README.md and each resource license before redistributing content.')
