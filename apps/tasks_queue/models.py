from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class QueuedTasks(models.Model):
    
    pickled_task = models.CharField(max_length=5000) #max row 65535
    queued_on = models.DateTimeField(auto_now_add=True)
    
class SuccessTasks(models.Model):
    
    task_id = models.IntegerField()
    saved_on = models.DateTimeField(auto_now_add=True)

    
class FailedTasks(models.Model):
    
    task_id = models.IntegerField()
    exception = models.CharField(max_length=2048)
    saved_on = models.DateTimeField(auto_now_add=True) 

    
    
    