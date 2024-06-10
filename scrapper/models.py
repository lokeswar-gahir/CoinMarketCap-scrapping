from django.db import models
import json
# Create your models here.
class Job(models.Model):
    job_id = models.CharField(max_length=40)
    requested_for = models.JSONField('Requested For')
    time_stamp = models.DateTimeField("Time Stamp", auto_now_add=True)

    def __str__(self):
        return f'{self.job_id}'

class Task(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    coin = models.CharField(max_length=10)
    slug = models.CharField(max_length=30)
    data = models.JSONField("Json Data")

    def __str__(self):
        return f'{self.coin}'