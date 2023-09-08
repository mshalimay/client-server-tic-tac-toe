import socket
from server import HOST_ADDRESS

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# connect to the server on port 8000
client_socket.connect((HOST_ADDRESS, 8595))

# receive data from the server
data = client_socket.recv(1024)

# decode the received data and print it
print(data.decode())

# close the connection
client_socket.close()