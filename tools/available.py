import requests
import time
import json

BASE_URL='https://home.antoniuk.pl/api/'
AVAILABLE_AUDIO_SET_ENDPOINT=BASE_URL+'available_audio_set/'
DEBUG_ENDPOINT=BASE_URL+'debug/'
REQUEST_HEADERS={}

with requests.Session() as session:
    debug_secret = {'key': 'e329e6179a600391c749f5761fefd25b'}
    response = session.post(DEBUG_ENDPOINT, data=debug_secret, headers=REQUEST_HEADERS)
    print(f'DEBUG_ENDPOINT response: {response}')

    available_audio_sets = {}
    response = session.get(AVAILABLE_AUDIO_SET_ENDPOINT, headers=REQUEST_HEADERS)
    try:
        parsed = response.json()
        for audio_set in parsed:
            print(audio_set)
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

    print('########## available_audio_sets ##########')
    for audio_set_id, audio_set_info in available_audio_sets.items():
        print(f'{"L" if audio_set_info["is_locked"] else " "} [{audio_set_id}]:\t layer: {audio_set_info["priority"]}\t locked_at: {audio_set_info["locked_at"]}') 
    print(f'count all:      {len(available_audio_sets)}')
    print(f'count locked:   {len(locked_audio_sets)}')
    print(f'count unlocked: {len(unlocked_audio_sets)}')

