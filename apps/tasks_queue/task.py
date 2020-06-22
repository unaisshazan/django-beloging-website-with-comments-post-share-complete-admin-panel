

class Task(object):
    
    def __init__(self,a_callable,*args,**kwargs):
        
        assert callable(a_callable)
        self.task_callable = a_callable
        self.args = args
        self.kwargs = kwargs
        self.db_id = None
    
    def run(self):
        self.task_callable(*self.args,**self.kwargs)
