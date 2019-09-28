from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status, views
from rest_framework.response import Response
import data_collector.serializers as serializers
import data_collector.models as models
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from rest_framework.parsers import FormParser,MultiPartParser
from django.core.exceptions import PermissionDenied
from rest_framework.utils import json

class PollDataViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    queryset = models.PollData.objects.all()
    serializer_class = serializers.PollDataSerialier

    def create(self, request, *args, **kwargs):
        data = {**request.data}
        data['user_info']['user_agent'] = request.META['HTTP_USER_AGENT']
        data['user_info']['ip_address'] = request.META['REMOTE_ADDR']
        data['assigned_set'] = data['assigned_set_id']

        try:
            models.AvailableAudioSet.complete(data['assigned_set_id'])
            serializer = serializers.PollDataSerialier(data=data)        
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except models.AudioSetCompleteError as e:
            response = {'code': e.code, 'message': str(e)}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        serializer = serializers.PollDataSerialier(self.queryset, many=True)
        return Response(serializer.data)
    
class AudioSetViewSet(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    
    queryset = models.AudioSet.objects.all()
    serializer_class = serializers.AudioSetSerializer

    def retain(self, request, seed, *args, **kwargs):
        samples = models.AvailableAudioSet.retain(seed)     
        return Response(samples)
    
    def renew(self, request, *args, **kwargs):
        try:
            models.AvailableAudioSet.renew(request.data['set_id'])
            return Response(status=status.HTTP_200_OK)
        except models.AudioSetCompleteError as e:
            response = {'code': e.code, 'message': str(e)}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        serializer = serializers.AudioSetSerializer(self.queryset, many=True)
        return Response(serializer.data)

class CommentViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = serializers.CommentSerializer(data=request.data)        
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ProblemViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    
    queryset = models.Problem.objects.all()
    serializer_class = serializers.ProblemSerializer

    def create(self, request, *args, **kwargs):
        data = {**request.data}
        data['user_info']['user_agent'] = request.META['HTTP_USER_AGENT']
        data['user_info']['ip_address'] = request.META['REMOTE_ADDR']

        serializer = serializers.ProblemSerializer(data=data)        
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SummaryAnswersView(views.APIView):
    def get(self, request, pk=None, *args, **kwargs):
        summary = models.PollData.summary(pk)        
        result = serializers.SummarySerializer(summary, many=True).data
        return Response(result)

class SummaryAudioSetsView(views.APIView):
    def get(self, request, *args, **kwargs):
        audio_set_summary = models.AudioSet.summary()
        return Response(audio_set_summary)

class LogView(views.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(LogView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):        
        log = models.LogMessage()
        log.user_agent = request.META.get('HTTP_USER_AGENT')
        log.ip_address = request.META.get('REMOTE_ADDR')
        log.message_type = request.META.get('HTTP_MESSAGE_TYPE')
        log.message = request.body
        log.save(force_insert=True)
        return HttpResponse(status=201)

class VersionView(views.APIView):
    def get(self, request, *args, **kwargs):        
        result = {'version': '2.0.0'}
        return Response(result)

class AuthView(views.APIView):
    @classmethod
    def auth(cls, request, *args, **kwargs):
        try:
            request_data = json.loads(request.body)
        except json.json.JSONDecodeError:
            return False
        if request_data is None:
            return False
        return models.verify_captcha(request_data['captcha_response'])
    
    def post(self, request, *args, **kwargs): 
        request.session['auth'] = True
        return Response(status=status.HTTP_201_CREATED)
