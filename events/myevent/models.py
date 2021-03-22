from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    location = models.ForeignKey('Location', related_name='event_location', on_delete=models.CASCADE)

class Location(models.Model):
    lattitude = models.FloatField()
    altitude = models.FloatField()

class EventMember(models.Model):
    user_id = models.IntegerField()
    event = models.ForeignKey('Event', related_name='event', on_delete=models.CASCADE)
