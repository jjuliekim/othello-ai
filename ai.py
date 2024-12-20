import time

# icons/colors for board
WHITE_CIRCLE = '●'
BLACK_CIRCLE = '○'

# weighted heuristic sum
def weightedHeuristic(board, color):
  piece_score = piece_difference(board, color)
  corner_score = corner_control(board, color)
  edge_score = edge_control(board, color)
  mobility_score = len(mobility(board, color))
  corner_adj_score = corner_adjacent(board, color)
  return piece_score + (corner_score * 5) + (edge_score * 3) + mobility_score + (corner_adj_score * 2)

# +1 for player piece, -1 for opponent piece
def piece_difference(board, color):
  count = 0
  for i in range(8):
    for j in range(8):
      if board[i][j] == color:
        count += 1
      elif board[i][j] != ' ':  # opponent piece
        count -= 1
  return count

# +1 for player piece in corner, -1 for opponent piece in corner
def corner_control(board, color):
  score = 0
  corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
  for i, j in corners:
    if board[i][j] == color:
      score += 1
    elif board[i][j] != ' ':
      score -= 1
  return score

# +1 for player piece in edge, -1 for opponent piece in edge
def edge_control(board, color):
  score = 0
  edges = [(0, i) for i in range(8)] + [(7, i) for i in range(8)] + [(i, 0) for i in range(8)] + [(i, 7) for i in range(8)]
  for i, j in edges:
    if board[i][j] == color:
      score += 1
    elif board[i][j] != ' ':
      score -= 1
  return score

# -1 for player piece adjacent to corner, +1 for opponent piece adjacent to corner
def corner_adjacent(board, color):
  score = 0
  corner_adj = [(0, 1), (1, 0), (1, 1), (0, 6), (1, 7), (1, 6), 
                (6, 0), (6, 1), (7, 1), (6, 7), (7, 6), (6, 6)]
  for i, j in corner_adj:
    if board[i][j] == color:
      score -= 1
    elif board[i][j] != ' ':
      score += 1
  return score
  
# get all available moves
def mobility(board, color):
  moves = []
  for i in range(8):
    for j in range(8):
      if board[i][j] == ' ':  # move must be on an empty space
        if isValidMove(board, i, j, color):
          moves.append((i, j))
  return moves  # i = row, j = column

# check if move is valid
def isValidMove(board, row, col, color):
  opponent_color = BLACK_CIRCLE if color == WHITE_CIRCLE else WHITE_CIRCLE
  directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # up, down, left, right
                (-1, -1), (-1, 1), (1, -1), (1, 1)]  # diagonals
  # check all directions
  for i, j in directions:
    next_i = row + i
    next_j = col + j
    opponent_piece = False
    # check if there is an opponent piece in the direction
    while 0 <= next_i < 8 and 0 <= next_j < 8 and board[next_i][next_j] == opponent_color:
      next_i += i
      next_j += j
      opponent_piece = True
    # sequence has to end with player's piece
    if opponent_piece and 0 <= next_i < 8 and 0 <= next_j < 8 and board[next_i][next_j] == color:
      return True
  return False

# update discs after turn
def updateDiscs(board, coordinate, color, opponent_color):
  directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # up, down, left, right
                (-1, -1), (-1, 1), (1, -1), (1, 1)]  # diagonals
  # flip discs in all directions
  for i, j in directions:
    next_i = coordinate[0] + i
    next_j = coordinate[1] + j
    flip = []
    # check if there is an opponent piece in the direction
    while 0 <= next_i < 8 and 0 <= next_j < 8 and board[next_i][next_j] == opponent_color:
      flip.append((next_i, next_j))
      next_i += i
      next_j += j
    # if reaches player's piece, end search and flip pieces
    if 0 <= next_i < 8 and 0 <= next_j < 8 and board[next_i][next_j] == color:
      for row, col in flip:
        board[row][col] = color
        
# track board states that have already been evaluated
transposition_table = {}

# minimax algorithm
def minimax(board, depth, is_max_player, color, alpha, beta):
  # check if board state has already been evaluated
  board_state = str(board)
  if (board_state, depth, is_max_player) in transposition_table:
    return transposition_table[(board_state, depth, is_max_player)]

  available_moves = mobility(board, color)
  if depth == 0 or available_moves == []:
    result = (weightedHeuristic(board, BLACK_CIRCLE), None)
    transposition_table[(board_state, depth, is_max_player)] = result
    return result
  
  best_move = None
  if is_max_player: 
    max_eval = float('-inf')
    for move in available_moves:  # test all possible moves
      new_board = [row.copy() for row in board]
      new_board[move[0]][move[1]] = BLACK_CIRCLE
      updateDiscs(new_board, move, BLACK_CIRCLE, WHITE_CIRCLE)
      eval, _ = minimax(new_board, depth - 1, False, WHITE_CIRCLE, alpha, beta)
      if eval > max_eval:
        max_eval = eval
        best_move = move
      alpha = max(alpha, eval)
      if beta <= alpha:
        break
    result = (max_eval, best_move)
  else:  
    min_eval = float('inf')
    for move in available_moves:
      new_board = [row.copy() for row in board]
      new_board[move[0]][move[1]] = WHITE_CIRCLE
      updateDiscs(new_board, move, WHITE_CIRCLE, BLACK_CIRCLE)
      eval, _ = minimax(new_board, depth - 1, True, BLACK_CIRCLE, alpha, beta)
      if eval < min_eval:
        min_eval = eval
        best_move = move
      beta = min(beta, eval)
      if beta <= alpha:
        break
    result = (min_eval, best_move)
  # store result in transposition table
  transposition_table[(board_state, depth, is_max_player)] = result
  return result
  
# get best move
def getBestMove(board, depth):
  # iterative deepening
  start_time = time.time()
  for depth in range(1, depth + 1):  
    time_taken = time.time() - start_time
    if time_taken > 5:
      break
    _, move = minimax(board, depth, True, BLACK_CIRCLE, float('-inf'), float('inf'))
    if move is not None:
      best_move = move
  return best_move