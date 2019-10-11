import requests
import time
import json
import datetime

BASE_URL='https://home.antoniuk.pl/api/'
RETAIN_ENDPOINT=BASE_URL+'retain/'
DEBUG_ENDPOINT=BASE_URL+'debug/'
REQUEST_HEADERS={}

audio_retains = {}
retained_sets = []
retain_fails = []

with requests.Session() as session:
    debug_secret = {'key': 'e329e6179a600391c749f5761fefd25b'}
    response = session.post(DEBUG_ENDPOINT, data=debug_secret, headers=REQUEST_HEADERS)
    print(f'DEBUG_ENDPOINT response: {response}')

    for idx in range(80):
        response = session.get(RETAIN_ENDPOINT, headers=REQUEST_HEADERS)
        if response.status_code != 200:
            print(f'Retain error: {response}')
            break
        
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
