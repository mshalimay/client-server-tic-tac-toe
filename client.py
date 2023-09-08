# Client for TicTacToe game


# import modules and global variables
import socket
import sys
import pickle
from server import HOST_ADDRESS, validate_port


# ----------------------------------------
# Server class 
#-----------------------------------------
# Provides services to open/close client, connect and send/receive messages to server
class Client():
    def __init__(self, host_address:str, port:int):
        """ Initiate the class and create the client socket
        Args:
            host_address (str): the host address, such as "0.0.0.0"
            port (int): the port, such as '8080'
        """
        self.host = host_address
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connect_to_server(self):
        """ Connect to the server"""
        self.client.connect((self.host, self.port))


    def send_move(self, player:str, coordinates:str):
        """ Format and encode client move and send it to the server
        Args:
            player (str): "X" or "O"
            coordinates (_type_): the coordinates of the move, such as "(0, 1)"
        """
        # convert coordinates to a tuple
        coordinates_tuple = (int(coordinates[1]), int(coordinates[3]))

        # convert player name to uppercase and send message to server using pickle
        self.client.send(pickle.dumps((player.upper(), coordinates_tuple)))

    def receive_message(self) -> str:
        """receive and decode message from server using pickle
        """
        message = self.client.recv(1024)
        return pickle.loads(message)

    def close_client(self):
        self.client.close()

#-----------------------------------------
# Helper functions
#-----------------------------------------
def validate_coordinates(coordinates:str) -> str:
    """ Check if coordinates are in the correct format and within the gameboard
    Args:
        coordiantes (str): the coordinates of client move, such as "(0, 1)"
    Returns:
        str: an error message if the coordinates are invalid, otherwise an empty string
    """
   
    # check if coordinates are in the correct format
    if coordinates[0] != "(" or coordinates[-1] != ")":
        return "Error: Invalid move format. Move should be in the format (x, y)."
    # check if coordinates are integers
    try:
        x = int(coordinates[1])
        y = int(coordinates[3])
    except:
        return "Error: Invalid move format. x and y must be integers between 0 and 2 (inclusive))"
    # check if coordinates are within the gameboard
    if x < 0 or x > 2 or y < 0 or y > 2:
        return "Error: Invalid move format. x and y must be integers between 0 and 2 (inclusive))"
    return ""

def print_usage() -> None:
    """ Print usage message to the user
    """
    print("Error: Invalid number of arguments.\nUsage: python client.py <port> <player> <coordinate>\n"
              + "\nWhere:\nport: integer between 1024 and 64000\n"
              + "player: characters X or O\n"
              + "coordinate: string (x,y) representing a coordinate in the TicTacToe board, "
              +"where x and y are between 0 and 2 (inclusive)")

def validate_port(port:str) -> str:
    """ Validates the port number inputed by user, returning an error message if it is invalid
    Valid port number = integer between 1024 and 65535
    """
    if not port.isdigit() or int(port) < 1024 or int(port) > 65535:
        return "Please enter a port number between 1024 and 65535."
    return ""

#-----------------------------------------
# Main 
#-----------------------------------------
if __name__ == "__main__":
    # check if three arguments were provided; if not, print usage message and exit
    if len(sys.argv) != 4:
        print_usage()
        sys.exit(1)

    # retrieve CMD arguments; removing spaces from coordinates
    port = sys.argv[1]
    player = sys.argv[2]
    coordinates = sys.argv[3].replace(" ", "") 

    # check if port input is valid; if not, print error message and exit
    error_message = validate_port(port)
    if len(error_message) > 0:
        print(error_message)
        sys.exit(1)

    # check if player input is valid; if not, print error message and exit
    if player.upper() != "X" and player.upper() != "O":
        print("Error: Invalid player. Player must be either X or O")
        sys.exit(1)

    # check if coordinates input is valid; if not, print error message and exit
    error_message = validate_coordinates(coordinates)
    if len(error_message) > 0:
        print(error_message)
        sys.exit(1)

    # instantiate client and try to connect to server; if connection fails, print error message and exit
    client = Client(HOST_ADDRESS, int(port))
    try:
        client.connect_to_server()
    except:
        print("Error: Could not connect to server." +
              "\nPlease make sure the server is running and that you are connecting to the right port.")
        sys.exit(1)

    # send move to server and print response
    client.send_move(player, coordinates)
    print(client.receive_message())
    client.close_client()
    
    
    

