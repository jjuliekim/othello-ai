import board
import time
import ai

board.initBoard()
board.displayBoard()

player_turn = True  # False = computer move
WHITE_CIRCLE = '●'
BLACK_CIRCLE = '○'

# count pieces
def countPieces():
  white = 0
  black = 0
  for i in range(8):
    for j in range(8):
      if board.board[i][j] == WHITE_CIRCLE:
        white += 1
      elif board.board[i][j] == BLACK_CIRCLE:
        black += 1
  return white, black

while True:
  # check if game is over
  player_moves = board.getAvailableMoves(WHITE_CIRCLE)
  computer_moves = board.getAvailableMoves(BLACK_CIRCLE)
  if player_moves == [] and computer_moves == []:
    white, black = countPieces()
    if white > black:
      print(f"RESULT: PLAYER WINS! [{white}] - [{black}]")
    elif black > white:
      print(f"RESULT: COMPUTER WINS! [{black}] - [{white}]")
    else:
      print(f"RESULT: TIE! [{white}] - [{black}]")
    break
  
  # continue game
  if player_turn:  # player turn
    if player_moves == []:
      print('NO MOVES AVAILABLE. COMPUTER TURN.')
    else:
      if board.playerMove() is None:
        break
  else:  # computer turn
    time.sleep(1)
    if computer_moves == []:
      print('NO MOVES AVAILABLE. PLAYER TURN.')
    else:
      move = ai.getBestMove(board.board, 3)  # max depth = 3 for now
      print('COMPUTER MOVE: ', chr(move[1] + 65) + str(move[0] + 1))
      board.board[move[0]][move[1]] = BLACK_CIRCLE
      board.updateDiscs(move, BLACK_CIRCLE, WHITE_CIRCLE)
      
  # print updated board
  board.displayBoard()
  player_turn = not player_turn
  