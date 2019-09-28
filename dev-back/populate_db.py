import glob
import mysql.connector
import os
import random

AUDIO_SET_SIZE = 10

db = mysql.connector.connect(
        host=os.environ['BINPOLL_DB_HOST'],
        port=os.environ['BINPOLL_DB_PORT'],
        user=os.environ['BINPOLL_DB_USER'],
        passwd=os.environ['BINPOLL_DB_PASS'],
        database=os.environ['BINPOLL_DB_NAME'])

cursor = db.cursor()

sql_select_audioset = 'select count(*) from data_collector_audioset'
sql_insert_audiosample = 'insert into data_collector_audiosample (filepath) values (%s)'
sql_insert_audioset = 'insert into data_collector_audioset (use_count, priority) values (0, %s)'
sql_insert_available_audioset = 'insert into data_collector_availableaudioset (locked_at, audio_set_id) values (\'1000-01-01 00:00:00\', %s)'
sql_insert_audioset_samples = 'insert into data_collector_audioset_samples (audioset_id, audiosample_id) values (%s, %s)'

def insert_filenames(brir_filenames):
    for brir, filenames in brir_filenames.items():
        for filename in filenames:
            cursor.execute(sql_insert_audiosample, (filename,))

def insert_audioset(filenames, priority):
    for audioset_idx in range(len(filenames) // AUDIO_SET_SIZE):
        cursor.execute(sql_insert_audioset, (priority,))
        audioset_id = cursor.lastrowid
        cursor.execute(sql_insert_available_audioset, (audioset_id,))

        for filename_idx in range(AUDIO_SET_SIZE):
            filename = filenames[audioset_idx * AUDIO_SET_SIZE + filename_idx]
            cursor.execute(sql_insert_audioset_samples, (audioset_id, filename))
            print('inserted ', filename)

def get_brir_filenames():
    brir_filenames = {}
    for file in glob.glob('poll_sounds/*'):
        filename = os.path.basename(file)
        brir = filename.split('_')[-3]
        filename = '_'.join(filename.split('_')[:-2])
        if brir in brir_filenames:
            brir_filenames[brir].add(filename)
        else:
            brir_filenames[brir] = set()
            brir_filenames[brir].add(filename)
    
    for brir, filenames in brir_filenames.items():
        filenames = list(filenames)
        random.Random(125).shuffle(filenames)
        brir_filenames[brir] = filenames

    return brir_filenames

cursor.execute(sql_select_audioset)
(number_of_rows,) = cursor.fetchone()
if number_of_rows == 0:
    brir_filenames = get_brir_filenames()
    insert_filenames(brir_filenames)
    for priority in [0, 1, 2]:
        for brir, filenames in brir_filenames.items():
            insert_audioset(filenames, priority)

    db.commit()
