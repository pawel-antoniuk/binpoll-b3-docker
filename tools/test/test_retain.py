import requests
import time
import json
import datetime

BASE_URL='https://home.antoniuk.pl/api/'
RETAIN_ENDPOINT=BASE_URL+'retain/'
SESSION_KEY='sessionid'
SESSION_VALUE='acwadpvo98fe6bbqu0paz85boza38gy3'
REQUEST_HEADERS={'Cookie': f'{SESSION_KEY}={SESSION_VALUE}'}

audio_retains = {}
retained_sets = []
retain_fails = []
for idx in range(80):
    response = requests.get(RETAIN_ENDPOINT, headers=REQUEST_HEADERS)
    parsed = response.json()
    now = str(datetime.datetime.now(datetime.timezone.utc))
    if parsed['state'] == 'ok':
        audio_retains.setdefault(parsed['setId'], []).append({'priority': parsed['priority'], 'retain_date': now})
        retained_sets.append({'setId': parsed['setId'], 'priority': parsed['priority'], 'retain_date': now})
    else:
        retain_fails.append({'retain_date': now})

audio_retains = dict(sorted(audio_retains.items()))

with open('test_retain_output.txt', 'w') as f:
    f.write('########## audio_retains ##########\n')
    f.write(f'count: {len(audio_retains)}\n')
    f.write(f'{json.dumps(audio_retains, indent=2)}\n')

    f.write('########## retained_sets ##########\n')
    f.write(f'count: {len(retained_sets)}\n')
    f.write(f'{json.dumps(retained_sets, indent=2)}\n')

    f.write('########## retain_fails ##########\n')
    f.write(f'count: {len(retain_fails)}\n')
    f.write(f'{json.dumps(retain_fails, indent=2)}\n')
