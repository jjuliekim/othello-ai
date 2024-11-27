import random


board = [[" " for i in range(8)] for j in range(8)]
WHITE_CIRCLE = '●'
BLACK_CIRCLE = '○'

# initialize board
def initBoard():
  print('\nPlayer = WHITE (○), Computer = BLACK (●)')
  print('Enter "quit" to end game')
  print('Enter move in format "A1"')
  board[3][3] = WHITE_CIRCLE
  board[4][4] = WHITE_CIRCLE
  board[3][4] = BLACK_CIRCLE  # black discs
  board[4][3] = BLACK_CIRCLE

# print out board with borders and discs
def displayBoard():
  print('  A B C D E F G H')
  print(' -----------------')
  for i in range(8):
    print(i+1, end="|")
    for j in range(8):
      print(board[i][j], end="|")
    print()
  print(' -----------------\n')
  
# computer move (random for now)
def computerMove():
  move = random.choice(getAvailableMoves(BLACK_CIRCLE))
  print('COMPUTER MOVE: ', chr(move[1] + 65) + str(move[0] + 1))
  board[move[0]][move[1]] = BLACK_CIRCLE
  updateDiscs(move, BLACK_CIRCLE, WHITE_CIRCLE)

# player move
def playerMove():
  while True:
    move = input('PLAYER MOVE: ').upper()
    if (move == 'QUIT'):
      return None
    # check if player move is valid
    if len(move) == 2 and move[0] in 'ABCDEFGH' and move[1] in '12345678':
      coordinate = (int(move[1]) - 1, ord(move[0]) - 65)
      if coordinate in getAvailableMoves(WHITE_CIRCLE):
        board[coordinate[0]][coordinate[1]] = WHITE_CIRCLE
        updateDiscs(coordinate, WHITE_CIRCLE, BLACK_CIRCLE)
        return True
      else:
        print('[INVALID MOVE] Must be a valid move')
    else:
      print('[INVALID FORMAT] Must be in bounds and in format "A1"')
      
# check if move is valid
def isValidMove(row, col, color):
  opponent_color = BLACK_CIRCLE if color == WHITE_CIRCLE else WHITE_CIRCLE
  directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # up, down, left, right
                (-1, -1), (-1, 1), (1, -1), (1, 1)]  # diagonals
  # check all directions
  for i, j in directions:
    new_i = row + i
    new_j = col + j
    opponent_piece = False
    # check if there is an opponent piece in the direction
    while 0 <= new_i < 8 and 0 <= new_j < 8 and board[new_i][new_j] == opponent_color:
      new_i += i
      new_j += j
      opponent_piece = True
    # sequence has to end with player's piece
    if opponent_piece and 0 <= new_i < 8 and 0 <= new_j < 8 and board[new_i][new_j] == color:
      return True
  return False
  
# get available moves
def getAvailableMoves(color):
  moves = []
  for i in range(8):
    for j in range(8):
      if board[i][j] == ' ':  # move must be on an empty space
        if isValidMove(i, j, color):
          moves.append((i, j))
  return moves  # i = row, j = column

# update discs after turn
def updateDiscs(coordinate, color, opponent_color):
  # flip discs in all directions
  directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # up, down, left, right
                (-1, -1), (-1, 1), (1, -1), (1, 1)]  # diagonals
  for i, j in directions:
    new_i = coordinate[0] + i
    new_j = coordinate[1] + j
    flip = []
    # check if there is an opponent piece in the direction
    while 0 <= new_i < 8 and 0 <= new_j < 8 and board[new_i][new_j] == opponent_color:
      flip.append((new_i, new_j))
      new_i += i
      new_j += j
    # if reaches player's piece, end search and flip pieces
    if 0 <= new_i < 8 and 0 <= new_j < 8 and board[new_i][new_j] == color:
      for row, col in flip:
        board[row][col] = color
    