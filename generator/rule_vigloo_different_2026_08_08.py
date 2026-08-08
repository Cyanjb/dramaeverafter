import csv, io, os
D = '/workspace/dramaeverafter/data/'
p = D + 'match_queue.csv'
raw = open(p, 'rb').read()
c = raw.count(b'\r\n')
term = '\r\n' if c > raw.count(b'\n') - c else '\n'
q = list(csv.DictReader(open(p, newline='', encoding='utf-8')))

ruled = 0
for r in q:
    if (r.get('status') or '').lower().startswith('confirmed'):
        continue
    if 'vigloo' in r['candidate_b'].lower() and 'other platform' in r['candidate_a']:
        r['status'] = 'confirmed_different (Cyan, 2026-08-08)'
        ruled += 1
        print(f"  DIFFERENT: {r['candidate_a'][:56]}")

buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=list(q[0].keys()), lineterminator=term)
w.writeheader()
w.writerows(q)
open(p, 'w', newline='', encoding='utf-8').write(buf.getvalue())
print(f"\nruled {ruled} Vigloo rows as confirmed_different")

from collections import Counter
print("queue status now:", Counter((r.get('status') or '(blank)').split(' (')[0] for r in q).most_common())
