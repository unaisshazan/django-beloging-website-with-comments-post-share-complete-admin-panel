import socket
import sys
from app_settings import TASKS_HOST,TASKS_PORT
    
def send_data():

    data = sys.argv[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TASKS_HOST, TASKS_PORT))
    sock.send(data)
    received = sock.recv(1024)
    sock.close()
    print "Sent: %s" % data
    print "Received: %s" % received
    
if __name__ == "__main__":
    send_data()
    
