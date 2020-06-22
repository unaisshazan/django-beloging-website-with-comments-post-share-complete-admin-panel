import socket
from app_settings import TASKS_HOST,TASKS_PORT
    
def stop_server():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TASKS_HOST, TASKS_PORT))
    sock.send("stop")
    received = sock.recv(1024)
    sock.close()
    print "Sent: %s" % "stop"
    print "Received: %s" % received
    
if __name__ == "__main__":
    stop_server()