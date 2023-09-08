# References
# socket library documentation: https://docs.python.org/3/library/socket.html

# socket.send(): https://pythontic.com/modules/socket/send

import pickle
import socket
import threading
import random

class Server():
    # initialize the class
    def __init__(self, host_address, port):
        self.host = host_address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.clients = {}
        self.gameboard = [[None, None, None], [None, None, None], [None, None, None]]
        self.last_move = None

    # handle connections
    def accept_client(self) -> None:
        while True:
            client, address = self.socket.accept()
            if len(self.clients) <= 2:
                # assign X or O to client
                client_name = self.assign_X_O()
                self.clients[client_name] = client
                thread = threading.Thread(target=self.send_receive_client_message, args=(client, client_name))
                thread.start()
            else:
                # send message to client that server is full
                client.send("Sorry, the server is full!".encode("utf-8"))
                client.close()
        
    def send_receive_client_message(self, client: socket.socket, client_name: str):
        # send welcome message to client
        client.send(f"Welcome to Tic Tac Toe!\nYou will be playing with {client_name}".encode("utf-8"))

        while True:
            # receive message from client
            move = pickle.loads(client.recv(1024))

            
            # check if client sent a valid move
            error_message = self.validate_move(move, client_name)

            # if client sent an invalid move, send error message to client; 
            # otherwise, update gameboard and send it to client
            
            if len(error_message)>0:
                # send message to client that move is invalid
                client.send(error_message.encode("utf-8"))
            else:
                # update gameboard
                self.update_board(move)
                self.check_winner()



                # send updated gameboard to client
                client.send(pickle.dumps(self.board_to_string()))
            
    def update_board(self, move) -> None:
        self.gameboard[move[1][0]][move[1][1]] = move[0]


    def check_winner(self) -> str:
        pass
     
        
    def board_to_string(self) -> str:
        board_string = ""
        for row in self.gameboard:
            for col in row:
                board_string += col if col != None else " "
            board_string += "\n"
        return board_string
                
    def validate_move(self, move, client_name: str) -> str:
        if move[0].lower() != client_name.lower():
            return "Invalid move: you should be playing with " + client_name
        elif self.gameboard[move[1][0]][move[1][1]] != None:
            return "Invalid move: this spot is already occupied"
        return ""      
        
    def check_turn(self, client_name: str) -> bool:

        
        
    def assign_X_O(self) -> str:
        # randomly assign X or O to client
        if len(self.clients) == 1:
            return "X" if random.randint(0, 1) == 0 else "O"          
        else:
            return "X" if self.clients[0] == "O" else "O"
            
        
##----------------------------------------------
# testing

gameboard = [["X", "X", "X"], [None, "O", None], [None, None, "X"]]


def board_to_string(gameboard) -> str:
    board_string = ""
    for row in gameboard:
        board_string += "| "
        for col in row:
            board_string += col if col != None else " "
            board_string += " | "
        board_string += "\n"
    return board_string

def check_winner(gameboard):
    print(board_to_string(gameboard))
    for row in gameboard:
        if row[0] == row[1] == row[2] and row[0] != None:
            print(f"{row[0]} wins!")
            return
    for col in range(3):
        if gameboard[0][col] == gameboard[1][col] == gameboard[2][col] and gameboard[0][col] != None:
            print(f"{gameboard[0][col]} wins!")
            return
    if gameboard[0][0] == gameboard[1][1] == gameboard[2][2] and gameboard[0][0] != None:
        print(f"{gameboard[0][0]} wins!")
        return
    print("No winner yet")
    
check_winner(gameboard)
