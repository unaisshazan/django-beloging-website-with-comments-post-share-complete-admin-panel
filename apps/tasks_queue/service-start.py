# run from shell with python -m and the full python path
# to allow relative imports
from .app_settings import TASKS_HOST,TASKS_PORT
from . import worker_manager
from .server import TaskSocketServerThread
import time

worker_manager.start()
server_thread = TaskSocketServerThread(TASKS_HOST,TASKS_PORT)
time.sleep(5)
socket_server = server_thread.socket_server()
socket_server.serve_forever()


