from gtts import gTTS
import re
import os
import glob
import sox

OUTPUT_FILE_LENGTH_SECONDS = 7

def title_to_speak(title, output_filepath):
    title = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', title)
    title = title.replace('_', ', ')
    title = os.path.splitext(title)[0]
    tts = gTTS(text=title, lang='en', slow=False)
    tts.save(output_filepath)

    return title

for filepath in glob.glob('input/*'):
    filename = os.path.basename(filepath)
    title_to_speak(filename, 'output/' + filename)