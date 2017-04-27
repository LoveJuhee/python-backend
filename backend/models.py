from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Center(models.Model):
    """
    관리하는 로컬관제센터, 피난유도시스템에 대한 객체
    """
    label = models.SlugField(unique=True)   # key
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.label

    class Meta:
        ordering = ('id',)


class Sensor(models.Model):
    """
    Center 모델에 설치되어 있는 센서에 대한 객체
    """
    name = models.CharField(max_length=50, default='unknown')
    model = models.CharField(max_length=50)
    serialnumber = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)


class Message(models.Model):
    """
    WebSocket 메시지 처리에 대한 객체
    """
    center = models.ForeignKey(Center, related_name='messages')
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return '[{timestamp}] {handle}: {message}', format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {'handle': self.handle,
                'message': self.message,
                'timestamp': self.formatted_timestamp}
