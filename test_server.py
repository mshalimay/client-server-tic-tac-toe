import socket
HOST = "0.0.0.0"
PORT = 8000



if __name__ == "__main__":
    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()

    # bind the socket to a public host, and a port
    server_socket.bind((HOST, PORT))

    # set the server to listen for incoming connections
    server_socket.listen(1)

    # wait for a client to connect
    print('Waiting for a client to connect')
    client_socket, address = server_socket.accept()
    print('Connected by', address)

    # send a message to the client
    message = 'Hello, client!'
    client_socket.sendall(message.encode())

    # close the connection
    client_socket.close()