# Short description
A simple tic-tac-toe game where clients connect to the server that mediates game. Uses `pickle` for serialization and `socket` for networking functions.

# Instructions

To start the server, run
`Python server.py <port>`
- `port` is the port for the server to bind to.

To make a move, run
`Python client.py <port> <player> <coordinate>`

- `port` is the port for the tic-tac-toe server
- `player` is `x` or `o`
- `coordinate` is the row-column (zero-based) for the move in the board

