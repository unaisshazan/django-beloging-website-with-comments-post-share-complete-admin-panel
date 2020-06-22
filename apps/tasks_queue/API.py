import socket
from .task import Task
from . import helpers
from .app_settings import TASKS_HOST,TASKS_PORT


def push_task_to_queue(a_callable,*args,**kwargs):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    new_task = Task(a_callable,*args,**kwargs)
    new_task = helpers.save_task_to_db(new_task) #returns with db_id
    sock.connect((TASKS_HOST, TASKS_PORT))
    sock.send(helpers.serielize(new_task))
    received = sock.recv(1024)
    sock.close()
    
    return received