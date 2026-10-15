"""Check unique source URLs and update catalog reachability metadata."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import urllib.request,urllib.error,json

ROOT=Path(__file__).resolve().parents[1]
def check(url):
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Prapawit-Learning-Catalog/1.0'},method='GET')
        with urllib.request.urlopen(req,timeout=12) as r:
            r.read(1024)
            return url,{'check_status':'reachable','http_status':r.status,'resolved_url':r.url}
    except urllib.error.HTTPError as e:
        status='not_found' if e.code in (404,410) else 'blocked_or_error'
        return url,{'check_status':status,'http_status':e.code}
    except Exception as e:
        return url,{'check_status':'unconfirmed','error_type':type(e).__name__}

if __name__=='__main__':
    p=ROOT/'catalog.json'; data=json.loads(p.read_text())
    urls=sorted({r['url'] for c in data['categories'] for r in c['resources']})
    with ThreadPoolExecutor(max_workers=10) as ex: results=dict(ex.map(check,urls))
    now=datetime.now(timezone.utc).isoformat()
    for c in data['categories']:
        for r in c['resources']: r.update(results[r['url']],checked_at=now)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'link-report.json').write_text(json.dumps({'checked_at':now,'unique_urls':len(urls),'results':results},indent=2)+'\n')
    counts={s:sum(r['check_status']==s for r in results.values()) for s in sorted({r['check_status'] for r in results.values()})}
    print(json.dumps({'unique_urls':len(urls),'status_counts':counts}))
    for u,r in results.items():
        if r['check_status']!='reachable': print(r['check_status'],r.get('http_status',r.get('error_type')),u)
