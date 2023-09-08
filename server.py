
# Server for Tic Tac Toe game

# import modules
import pickle
import socket
import random
import sys

# Host address for server and client
HOST_ADDRESS = "0.0.0.0"

# ----------------------------------------
# Server class 
#-----------------------------------------
# Provides services to deploy the server, connect and send/rece 
# messages from clients, and game logic 

class Server():
    # initialize the class
    def __init__(self, host_address, port):
        self.host = host_address
        self.port = port
        self.gameboard = [[None, None, None], [None, None, None], [None, None, None]]
        self.last_move = None   # "X" or "O"; last move to control who should play next
        self.num_moves = 0      # number of moves made; used to check for a tie


    def intialize_server(self):
        """ Create the server socket bind to the host address and port
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)       
        print(f"Server started on {self.server.getsockname()}")
        self.send_receive_client_message()
             
    def send_receive_client_message(self):
        """ Send and receive messages about the game to clients according to the
        results of the game after each client movement 
        """

        # infinte loop: listen to clients while the game is not finished
        while True:
            # accept client, # receive and decode the message using pickle
            client, address = self.server.accept()           
            move = pickle.loads(client.recv(1024))

            # check if client sent a valid move 
            error_message = self.validate_move(move)

            # if client sent an invalid move, send error message to client; 
            # otherwise, update gameboard and send it to client
            if len(error_message)>0:
                # send message to client that move is invalid
                client.send(pickle.dumps(error_message))
            else:
                # update control variables
                self.last_move = move[0]
                self.num_moves += 1

                # update gameboard and check for game result
                self.update_board(move)
                game_result = self.check_game_result()

                # if not win nor tie, inform to client move was received and send the board
                if len(game_result) == 0:
                    message = f"Your move was received. Current board:\n\n{self.board_to_string()}"
                    client.send(pickle.dumps(message))

                # if game is finished, inform to client the results
                else:
                    if game_result == "tie":
                        message = f"\nIt's a tie!\n\n{self.board_to_string()}"
                    else:
                        message = f"\nPlayer {game_result} has won the game!\n\n{self.board_to_string()}"
                    client.send(pickle.dumps(message))
                    break
        # if loop broke, game is finished so close the server
        self.server.close()
        return

    def update_board(self, move:list) -> None:
        """ Update TicTacToe board given a valid move from client
        Args:
            move (list): contains the type of move ("O" or "X") and its coordinates
        """
        self.gameboard[move[1][0]][move[1][1]] = move[0]

    def check_game_result(self) -> str:
        """Check if game is finished and return the result as a string

        Returns:
            str: "X" if player X won, "O" if player O won, "tie" if it's a tie, or "" if game is not finished
        """
        # check if there is a winner through the rows
        for row in self.gameboard:
            if row[0] == row[1] == row[2] and row[0] != None:
                return row[0]

        # check if there is a winner through the columns
        for col in range(3):
            if self.gameboard[0][col] == self.gameboard[1][col] == self.gameboard[2][col] and self.gameboard[0][col] != None:
                return self.gameboard[0][col] 

        # check if there is a winner through the right diagonal
        if self.gameboard[0][0] == self.gameboard[1][1] == self.gameboard[2][2] and self.gameboard[0][0] != None:
            return self.gameboard[0][0]

         # check if there is a winner through the left diagonal
        if self.gameboard[0][2] == self.gameboard[1][1] == self.gameboard[2][0] and self.gameboard[0][2] != None:
            return self.gameboard[0][2]

        # if no winner and all spots are occupied, it's a tie
            # @todo: this can be optimized; tie can be definite before all spots are occupied
        if self.num_moves == 9:
            return "tie"

        return ""
        
    def board_to_string(self) -> str:
        """ Convert the gameboard to a string to be send to client
        """
        board_string = ""
        for row in self.gameboard:
            board_string += "| "
            for col in row:
                board_string += col if col != None else " "
                board_string += " | "
            board_string += "\n"
        return board_string
        
                
    def validate_move(self, move:list) -> str:
        """ Validate the move sent by client
        Args:
            move (list): contains the type of move ("O" or "X") and its coordinates
        Returns:
            str: error message if move is invalid, or "" if move is valid
        """

        # check if it is the client's turn
        if move[0] == self.last_move:
            return "Please wait for your turn."
        # check if coordinate is already occupied
        elif self.gameboard[move[1][0]][move[1][1]] != None:
            return f"Move ({move[1][0]}, {move[1][1]}) is invalid. The spot is already occupied"
        return ""      

#------------------------------------------------------------
# helper functions
#------------------------------------------------------------
def validate_port(port:str) -> str:
    """ Validates the port number inputed by user, returning an error message if it is invalid
    Valid port number = integer between 1024 and 65535
    """
    if not port.isdigit() or int(port) < 1024 or int(port) > 65535:
        return "Please enter a port number between 1024 and 65535."
    return ""

#------------------------------------------------------------
# main 
#------------------------------------------------------------
if __name__ == "__main__":
    # check if three arguments were provided by user; return usage message if not
    if len(sys.argv) != 2:
        print("Please input a port number between 1024 and 64000.\nE.g.: python server.py 8282")
        sys.exit(1)

    # retrieve port number and validate it
    # Valid port = integer between 1024 and 65535
    port = sys.argv[1]
    error_message = validate_port(port)

    # if port number not valid, print error message and exit
    if len(error_message) > 0:
        print(error_message)
        sys.exit(1)  

    # instatiate the Server and try to initialize it; 
    # if not able to connect, print error message and exit
    server = Server(HOST_ADDRESS, int(port))
    try:
        server.intialize_server()
    except:    
        print("Error: Could not start server.\nPlease check the port number or try again later.")
        sys.exit(1)
        
    

    