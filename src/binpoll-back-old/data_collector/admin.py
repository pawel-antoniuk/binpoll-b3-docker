from django.contrib import admin
from . import models

admin.site.register(models.PollData)
admin.site.register(models.AudioSample)
admin.site.register(models.AudioSet)
admin.site.register(models.AvailableAudioSet)
admin.site.register(models.UserInfo)
admin.site.register(models.Problem)
admin.site.register(models.Comment)
admin.site.register(models.PollAnswer)
admin.site.register(models.LogMessage)

# Register your models here.
