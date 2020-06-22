from django.conf import settings


D = {"MAX_RETRIES":3,
     "TASKS_HOST":"localhost",
     "TASKS_PORT":8002}


if hasattr(settings,"TASKS_QUEUE"):
    for key,value in getattr(settings,"TASKS_QUEUE"):
        D[key] = value
        
        
MAX_RETRIES = D["MAX_RETRIES"]
TASKS_HOST = D['TASKS_HOST']
TASKS_PORT = D['TASKS_PORT']

