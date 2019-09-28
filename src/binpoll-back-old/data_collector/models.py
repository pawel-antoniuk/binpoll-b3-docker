from django.db import models, transaction
import lzma
import random
import datetime
from django.db.models import Max
from django.conf import settings
import requests

class AudioSample(models.Model):
    filepath = models.CharField(max_length=128, primary_key=True)

    def __str__(self):
        return 'Sample: {}'.format(self.filepath)

class AvailableAudioSet(models.Model):
    audio_set = models.OneToOneField('AudioSet', on_delete=models.CASCADE, primary_key=True)
    locked_at = models.DateTimeField(default=datetime.datetime.min)
  
    LOCK_TIMEOUT_MINUTES = 5

    def lock(self):
        self.locked_at = datetime.datetime.now(datetime.timezone.utc)

    def is_locked(self):
        return self.locked_at > (datetime.datetime.now(datetime.timezone.utc) 
                                - datetime.timedelta(minutes=self.LOCK_TIMEOUT_MINUTES))

    @classmethod
    def renew(self, audio_set_pk):
        with transaction.atomic():
            available_audio_set = (AvailableAudioSet.objects
                .select_related('audio_set').select_for_update()
                .filter(pk = audio_set_pk).first())
            if available_audio_set is None:
                raise AudioSetCompleteError('Audio set is not available', 3)

            available_audio_set.lock()
            available_audio_set.save()

    @classmethod
    def complete(cls, audio_set_pk):
        with transaction.atomic():
            available_audio_set = (AvailableAudioSet.objects
                .select_related('audio_set').select_for_update()
                .filter(pk = audio_set_pk).first())
            if available_audio_set is None:
                raise AudioSetCompleteError('Operation not permitted', 1)
            
            if not available_audio_set.is_locked():
                raise AudioSetCompleteError('Timeout', 2)
            else:
                available_audio_set.delete()
                available_audio_set.audio_set.use_count += 1
                available_audio_set.audio_set.save()
                
    @classmethod
    def retain(cls, seed):
        found = False  
        with transaction.atomic():
            for priority in [0, 1, 2]:
                available_audio_sets = (AvailableAudioSet.objects
                    .filter(locked_at__lte = datetime.datetime.now(datetime.timezone.utc) 
                                            - datetime.timedelta(minutes=cls.LOCK_TIMEOUT_MINUTES))
                    .filter(audio_set__priority = priority))
                if available_audio_sets.count() != 0:
                    found = True
                    random_idx = random.randint(0, available_audio_sets.count() - 1)
                    available_audio_set = available_audio_sets.select_related('audio_set').select_for_update()[random_idx]
                    available_audio_set.lock()
                    available_audio_set.save()
                    break
        
        if not found:
            retained_set = {}
            retained_set['state'] = 'fail'
            retained_set['reason'] = 'not available'
            return retained_set

        samples = list(available_audio_set.audio_set.samples.all())

        if seed == 0:
            seed = random.randint(1, 9999)
        rand = random.Random()
        rand.seed(seed)
        rand.shuffle(samples)

        retained_set = {}
        retained_set['state'] = 'ok'
        retained_set['seed'] = seed
        retained_set['set_id'] = available_audio_set.audio_set.pk
        retained_set['priority'] = available_audio_set.audio_set.priority
        retained_set['sampleNames'] = [s.filepath for s in samples]
        retained_set['samples'] = [rand.sample([s.filepath + '_scene1_FB.wav',
            s.filepath + '_scene2_BF.wav', s.filepath + '_scene3_FF.wav'], 3)  for s in samples]     

        return retained_set


class AudioSetCompleteError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code

class AudioSet(models.Model):
    id = models.AutoField(primary_key=True)
    samples = models.ManyToManyField(AudioSample)
    use_count = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)

    @classmethod
    def summary(cls):
        audio_set_summary = {}
        for audio_set in AudioSet.objects.order_by('priority').all():
            samples = [s.filepath for s in audio_set.samples.all()]
            audio_set_summary[audio_set.id] = {}
            audio_set_summary[audio_set.id]['priority'] = audio_set.priority
            audio_set_summary[audio_set.id]['count'] = len(samples)
            audio_set_summary[audio_set.id]['samples'] = samples
        return audio_set_summary

class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True)
    age = models.CharField(max_length=32)
    hearing_difficulties = models.BooleanField()
    listening_test_participated = models.BooleanField()
    headphones_make_and_model = models.CharField(max_length=512, blank=True, default='')

class PollData(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    seed = models.PositiveIntegerField()
    answers = models.ManyToManyField(AudioSample, through='PollAnswer')
    assigned_set = models.ForeignKey(AudioSet, on_delete=models.CASCADE)
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    @staticmethod
    def generate_answer(poll_datas, name, append_filter):
        answer = {}
        answer['sample'] = name
        answer['user_answers'] = []
        for poll_data in poll_datas:
            answer['user_answers'].append(append_filter(poll_data))
        return answer

    @classmethod
    def summary(cls, pk):
        answers = []
        audio_set = AudioSet.objects.get(pk=pk)
        poll_datas = PollData.objects.filter(assigned_set_id=pk)
        
        for sample in audio_set.samples.all():
            scenes = dict.fromkeys(['FB', 'BF', 'FF'], {'user_answers': []})
            scenes['FB']['sample'] = sample.filepath + '_scene1_FB.wav'
            scenes['BF']['sample'] = sample.filepath + '_scene2_BF.wav'
            scenes['FF']['sample'] = sample.filepath + '_scene3_FF.wav'

            for poll_data in poll_datas:
                poll_answer = PollAnswer.objects.get(sample_id=sample.filepath, poll_data_id=poll_data.pk)
                scenes['FB']['user_answers'].append(poll_answer.answer_FB)
                scenes['BF']['user_answers'].append(poll_answer.answer_BF)
                scenes['FF']['user_answers'].append(poll_answer.answer_FF)
            answers.extend([scenes['FB'], scenes['BF'], scenes['FF']])
        
        answers.append(PollData.generate_answer(poll_datas, 'answer_id',                     lambda poll_data : poll_data.id))
        answers.append(PollData.generate_answer(poll_datas, 'ip_addr',                       lambda poll_data : poll_data.user_info.ip_address))
        answers.append(PollData.generate_answer(poll_datas, 'start_date',                    lambda poll_data : poll_data.start_date))
        answers.append(PollData.generate_answer(poll_datas, 'age',                           lambda poll_data : poll_data.user_info.age))
        answers.append(PollData.generate_answer(poll_datas, 'hearing_difficulties',          lambda poll_data : poll_data.user_info.hearing_difficulties))
        answers.append(PollData.generate_answer(poll_datas, 'listening_test_participated',   lambda poll_data : poll_data.user_info.listening_test_participated))
        answers.append(PollData.generate_answer(poll_datas, 'headphones_make_and_model',     lambda poll_data : poll_data.user_info.headphones_make_and_model))

        return answers


class PollAnswer(models.Model):
    sample = models.ForeignKey(AudioSample, on_delete=models.CASCADE)
    poll_data = models.ForeignKey(PollData, on_delete=models.CASCADE)
    answer_FB = models.CharField(max_length=32)
    answer_BF = models.CharField(max_length=32)
    answer_FF = models.CharField(max_length=32)
    class Meta:
        unique_together = (("sample", "poll_data"),)
    def __str__(self):
        return 'Answer: FB: {}, BF: {}, FF: {}'.format(self.answer_FB, self.answer_BF, self.answer_FF)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    poll_data = models.ForeignKey(PollData, on_delete=models.CASCADE)
    message = models.TextField(max_length=1024)

    def __str__(self):
        return 'Comment: {}'.format(self.message)

class Problem(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField(max_length=1024)
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return 'Comment: {}'.format(self.message)

class LogMessage(models.Model):
    id = models.AutoField(primary_key=True)
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True)
    message = models.BinaryField(max_length=1024*1024, editable=True)
    message_type = models.CharField(max_length=64, blank=True, default='')
    
    def __str__(self):
        return 'Log: [{}] {}: {}'.format(self.message_type, self.ip_address, self.message.decode())
        
def verify_captcha(recaptcha_response):    
    request_data = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    response = requests.post(settings.GOOGLE_RECAPTCHA_URL, data=request_data).json()
    print(f'Google reCaptcha request: {request_data}')
    print(f'Google reCaptcha response: {response}')
    if response is None:
        return False

    return response['success']
