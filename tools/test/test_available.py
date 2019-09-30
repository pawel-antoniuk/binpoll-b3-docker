import requests
import time
import json

BASE_URL='https://home.antoniuk.pl/api/'
AVAILABLE_AUDIO_SET_ENDPOINT=BASE_URL+'available_audio_set/'
SESSION_KEY='sessionid'
SESSION_VALUE='i7tb0jjbv9g72219y87z2yljhbsm5q4b'
REQUEST_HEADERS={'Cookie': f'{SESSION_KEY}={SESSION_VALUE}'}

available_audio_sets = {}
response = requests.get(AVAILABLE_AUDIO_SET_ENDPOINT, headers=REQUEST_HEADERS)
parsed = response.json()
for audio_set in parsed:
    available_audio_sets[audio_set['audioSet']['id']] = {
        'is_locked': audio_set['isLocked'],
        'locked_at': audio_set['lockedAt']
    }

available_audio_sets = dict(sorted(available_audio_sets.items()))
locked_audio_sets = {k: v for k, v in available_audio_sets.items() if v['is_locked']}
unlocked_audio_sets = {k: v for k, v in available_audio_sets.items() if not v['is_locked']}

with open('test_available_output.txt', 'w') as f:
    f.write('########## available_audio_sets ##########\n')
    f.write(f'count all: \t{len(available_audio_sets)}\n')
    f.write(f'count locked: \t{len(locked_audio_sets)}\n')
    f.write(f'count unlocked: \t{len(unlocked_audio_sets)}\n')
    f.write(f'{json.dumps(available_audio_sets, indent=2)}\n')

