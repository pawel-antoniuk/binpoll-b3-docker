from rest_framework import serializers
from data_collector.models import PollData, AudioSet, AudioSample, Comment, UserInfo, Problem, PollAnswer, LogMessage

class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('id', 'user_agent', 'ip_address', 'age', 'hearing_difficulties',
                  'listening_test_participated', 'headphones_make_and_model')

class PollAnswerSerializer(serializers.HyperlinkedModelSerializer):
    sample = serializers.PrimaryKeyRelatedField(queryset=AudioSample.objects.all())
    poll_data = serializers.PrimaryKeyRelatedField(queryset=PollData.objects.all())
    class Meta:
        model = PollAnswer
        fields = ('id', 'sample', 'poll_data', 'answer_FB', 'answer_BF', 'answer_FF')

class PollDataSerialier(serializers.HyperlinkedModelSerializer):
    assigned_set = serializers.PrimaryKeyRelatedField(queryset=AudioSet.objects.all())
    user_info = UserInfoSerializer(many=False)
    answers = serializers.DictField(write_only=True)
    class Meta:
        model = PollData
        fields = ('id', 'start_date', 'end_date', 'seed', 'assigned_set', 'answers',
                  'user_info')
    def create(self, validated_data):
        user_info = validated_data.pop('user_info')
        user_info = UserInfo.objects.create(**user_info)
        user_info.save()

        answers_src = validated_data.pop('answers')
        validated_data['user_info_id'] = user_info.pk 
        poll_data = PollData.objects.create(**validated_data)
        poll_data.save()

        answers = []
        for filepath, value in answers_src.items():
            answers.append(PollAnswer(sample_id=filepath,
                poll_data_id=poll_data.pk,
                answer_FB=value['answer_FB'],
                answer_BF=value['answer_BF'],
                answer_FF=value['answer_FF']))
        PollAnswer.objects.bulk_create(answers)

        return poll_data

class AudioSampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AudioSample
        fields = ('filepath')

class AudioSetSerializer(serializers.HyperlinkedModelSerializer):
    # samples = AudioSampleSerializer(many=True, read_only=True)
    samples = serializers.SlugRelatedField(many=True, read_only=True, slug_field='filepath')
    class Meta:
        model = AudioSet
        fields = ('id', 'samples')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    poll_data = serializers.PrimaryKeyRelatedField(queryset=PollData.objects.all())
    class Meta:
        model = Comment
        fields = ('id', 'poll_data', 'message')

class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    user_info = UserInfoSerializer(many=False)
    class Meta:
        model = Problem
        fields = ('id', 'message', 'user_info')
    def create(self, validated_data):
        user_info = validated_data.pop('user_info')
        user_info_obj = UserInfo.objects.create(**user_info)
        user_info_obj.save()
        
        validated_data['user_info_id'] = user_info_obj.pk 
        problem = Problem.objects.create(**validated_data)
        UserInfo.objects.create(**user_info)
        return problem

# class AudioSampleSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = AudioSample
#         fields = ('id', 'filepath')


class SummarySerializer(serializers.Serializer):
    sample = serializers.CharField()
    user_answers = serializers.ListField(child=serializers.CharField())
