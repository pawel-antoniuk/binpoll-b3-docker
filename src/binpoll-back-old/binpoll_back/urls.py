"""binpoll_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from data_collector import views
from data_collector.models import PollData
from rest_framework.documentation import include_docs_urls
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'poll_data', views.PollDataViewSet)
router.register(r'audio_set', views.AudioSetViewSet)
router.register(r'comment', views.CommentViewSet)
router.register(r'problem', views.ProblemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('retain/', views.AudioSetViewSet.as_view({'get': 'retain'}), {'seed': 0}),
    path('renew/', views.AudioSetViewSet.as_view({'post': 'renew'})),
    path('admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='Binpoll API')),
    path('summary/answers/<int:pk>/', views.SummaryAnswersView.as_view()),
    path('summary/audiosets/', views.SummaryAudioSetsView.as_view()),
    path('log/', views.LogView.as_view()),
    path('version/', views.VersionView.as_view()),
    path('auth/', views.AuthView.as_view())
]
#urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'csv'])
