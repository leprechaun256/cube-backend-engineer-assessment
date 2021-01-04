from __future__ import unicode_literals

from django.db import models

from django.db import models
from django.contrib.postgres.fields import JSONField
# from django.contrib.gis.db.models import Point

# Create your models here.
    


class EndUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    
    @property
    def bills_paid(self):
        return len(self.events.filter(noun="bill"))


class EndUserEvent(models.Model):
    user = models.ForeignKey(EndUser, on_delete=models.CASCADE, related_name='events')
    properties = JSONField()
    ts_source = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)
    noun = models.TextField()
    verb = models.TextField()
    # lat_long = Point()
    time_spent = models.IntegerField(default=0)
