import requests
import time
import json

BASE_URL='https://home.antoniuk.pl/api/'
RETAIN_ENDPOINT=BASE_URL+'retain/'
SESSION_KEY='sessionid'
SESSION_VALUE='i7tb0jjbv9g72219y87z2yljhbsm5q4b'
REQUEST_HEADERS={'Cookie': f'{SESSION_KEY}={SESSION_VALUE}'}

audio_retains = {}
retained_sets = []
retain_fails = []
for idx in range(50):
    response = requests.get(RETAIN_ENDPOINT, headers=REQUEST_HEADERS)
    parsed = response.json()
    if parsed['state'] == 'ok':
        audio_retains.setdefault(parsed['setId'], []).append({'priority': parsed['priority'], 'retain_date': time.ctime()})
        retained_sets.append({'setId': parsed['setId'], 'priority': parsed['priority'], 'retain_date': time.ctime()})
    else:
        retain_fails.append({'retain_date': time.ctime()})

with open('output.txt', 'w') as f:
    f.write('########## audio_retains ##########\n')
    f.write(f'count: {len(audio_retains)}\n')
    f.write(f'{json.dumps(audio_retains, indent=2)}\n')

    f.write('########## retained_sets ##########\n')
    f.write(f'count: {len(retained_sets)}\n')
    f.write(f'{json.dumps(retained_sets, indent=2)}\n')

    f.write('########## retain_fails ##########\n')
    f.write(f'count: {len(retain_fails)}\n')
    f.write(f'{json.dumps(retain_fails, indent=2)}\n')
