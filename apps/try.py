from django.core.signals import request_started,request_finished
from django.dispatch import receiver

@receiver(request_started)
def started(sender):
    print sender

@receiver(request_finished)
def finished(sender):
    print sender