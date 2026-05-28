## Requirements
1. The Tic-Tac-Toe game should be played on a 3x3 grid.
2. Two players take turns marking their symbols (X or O) on the grid.
3. The first player to get three of their symbols in a row (horizontally, vertically, or diagonally) wins the game.
4. If all the cells on the grid are filled and no player has won, the game ends in a draw.
5. The game should have a user interface to display the grid and allow players to make their moves.
6. The game should handle player turns and validate moves to ensure they are legal.
7. The game should detect and announce the winner or a draw at the end of the game.

## Classes and methods

### Game
- switch player turns
- asks board to check state or update state

### Board
- stores grid (3x3 2D array)
- check if move is valid (move is within grid and cell is empty)
- check wins (horizontal, vertical, diagonal)
- check draws (if board is full)
- place symbols

### Player
- name
- symbol (O or X)

### Move
- row and column

