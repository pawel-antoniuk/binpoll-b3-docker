import requests
import time
import json

BASE_URL='https://home.antoniuk.pl/api/'
AVAILABLE_AUDIO_SET_ENDPOINT=BASE_URL+'available_audio_set/'
DEBUG_ENDPOINT=BASE_URL+'debug/'
REQUEST_HEADERS={}

with requests.Session() as session:
    debug_secret = {'key': 'binpoll@5'}
    response = session.post(DEBUG_ENDPOINT, data=debug_secret, headers=REQUEST_HEADERS)
    print(f'DEBUG_ENDPOINT response: {response}')

    available_audio_sets = {}
    response = session.get(AVAILABLE_AUDIO_SET_ENDPOINT, headers=REQUEST_HEADERS)
    try:
        parsed = response.json()
        for audio_set in parsed:
            available_audio_sets[audio_set['audioSet']['id']] = {
                'priority': audio_set['audioSet']['priority'],
                'is_locked': audio_set['isLocked'],
                'locked_at': audio_set['lockedAt'],
            }
    except json.JSONDecodeError as e:
        print(response)

    available_audio_sets = dict(sorted(available_audio_sets.items()))
    locked_audio_sets = {k: v for k, v in available_audio_sets.items() if v['is_locked']}
    unlocked_audio_sets = {k: v for k, v in available_audio_sets.items() if not v['is_locked']}

    with open('test_available_output.txt', 'w') as f:
        f.write('########## available_audio_sets ##########\n')
        f.write(f'count all: \t{len(available_audio_sets)}\n')
        f.write(f'count locked: \t{len(locked_audio_sets)}\n')
        f.write(f'count unlocked: \t{len(unlocked_audio_sets)}\n')
        f.write(f'{json.dumps(available_audio_sets, indent=2)}\n')

