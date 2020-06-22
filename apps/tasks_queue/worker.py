#  Based on the Worker class from Python in a nutshell, by Alex Martelli
import logging
import os
import sys
import threading
import Queue

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_repo.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "site_repo.settings"
import django

from . import app_settings
from . import helpers

class Worker(threading.Thread):
    def __init__(self,logger_name=None):
        
        threading.Thread.__init__(self, name="django-tasks-queue")
        self._stopevent = threading.Event()
        self.setDaemon(1)
        self.worker_queue = Queue.Queue()
        self.tasks_counter = 0
        if logger_name != None:
            self.logger = logging.getLogger(logger_name)
        else:
            self.logger = logging
        
        self.start()
        
    def put_task_on_queue(self,new_pickled_task):
        
        try:
            new_task = helpers.unpack(new_pickled_task)
            self.tasks_counter += 1
            self.worker_queue.put(new_task)
            return True,"sent"
        except Exception as e:
            return False,"Worker: %s"%e.message
    
    def run_task(self,task):
        
        for i in range(app_settings.MAX_RETRIES):
            try:
                task.run()
                break
            except:
                if i < app_settings.MAX_RETRIES - 1:
                    pass
                else:
                    raise
    
    def stop_thread(self, timeout=None):
        """ Stop the thread and wait for it to end. """
        if self.worker_queue != None:
            self._stopevent.set()
            self.logger.warn('Worker stop event set')
            return "Stop Set"
        else:
            return "Worker Off"        
    
    def ping(self):
        if self.worker_queue != None:
            return "I'm OK"
        else:
            return "Worker Off"
    
    def status_waiting(self):
        return self.worker_queue.qsize()
    
    def status_handled(self):
        # all, success & failes
        return self.tasks_counter
        
    def run(self):
        # the code until the while statement does NOT run atomicaly
        # a thread while loop cycle is atomic
        # thread safe locals: L = threading.local(), then L.foo="baz"
        django.setup()
        self.logger.info('Worker Starts')
        while not self._stopevent.isSet():
            if not self.worker_queue.empty():
                try:
                    task = self.worker_queue.get()
                    self.run_task(task)
                except Exception as e:
                    helpers.save_task_failed(task,e)
                else:
                    helpers.save_task_success(task)
                    
             
        self.worker_queue = None
        self.logger.warn('Worker stopped, %s tasks handled'%self.tasks_counter)
                
