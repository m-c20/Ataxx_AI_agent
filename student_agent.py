# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time
from helpers import random_move, execute_move, check_endgame, get_valid_moves, count_disc_count_change

@register_agent("student_agent")
class StudentAgent(Agent):
  """
  A class for your implementation. Feel free to use this class to
  add any helper functionalities needed for your agent.
  """

  def __init__(self):
    super(StudentAgent, self).__init__()
    self.name = "StudentAgent"

  class TimeoutException(Exception):
      pass

  def step(self, board, player, opponent):
    """
    Implement the step function of your agent here.
    You can use the following variables to access the chess board:
    - chess_board: a numpy array of shape (board_size, board_size)
      where 0 represents an empty spot, 1 represents Player 1's discs (Blue),
      and 2 represents Player 2's discs (Brown).
    - player: 1 if this agent is playing as Player 1 (Blue), or 2 if playing as Player 2 (Brown).
    - opponent: 1 if the opponent is Player 1 (Blue), or 2 if the opponent is Player 2 (Brown).

    You should return a tuple (r,c), where (r,c) is the position where your agent
    wants to place the next disc. Use functions in helpers to determine valid moves
    and more helpful tools.

    Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
    """

    self.start_time = time.time()
    self.max_depth = 10
    self.player = player
    self.opponent = opponent
    self.time_limit = 1.94
    self.best_move = random_move(board, player=self.player)
    self.best_utility = float('-inf')
    self.board = board
    self.branching_factor = 10 # Branching factor
    
    try:
      self.ids()
    except self.TimeoutException:
      pass

    # Returns the move allowing the maximum gain 
    
    return self.best_move




  def ids(self):

    # Get valid moves and reorder by quick evaluation

    valid_moves = get_valid_moves(self.board, self.player)
    if not valid_moves:
      return  # No valid moves available, pass turn
    

    # Initialize a utilities set
    utilities = {}
    for move in valid_moves:
      utilities[move] = count_disc_count_change(self.board, move, self.player)
    

    # Iterative deepening search
    for depth_limit in range(1, self.max_depth + 1):

      # Sort moves by computed utilities except first one, where moves are sorted by order_moves
      valid_moves = sorted(valid_moves, key = lambda x: utilities[x], reverse = True)
      valid_moves = valid_moves[:self.branching_factor]

      current_best_move = valid_moves[0]
      current_best_utility = utilities[current_best_move]

      for move in valid_moves:
        
        self.time_out() # Break out of loop and return
        
        simulated_board = self.board.copy()
        execute_move(simulated_board, move, self.player)
        utility = self.min_value(simulated_board, float('-inf'), float('inf'), depth_limit-1)

        if utility > current_best_utility:
          current_best_utility = utility
          current_best_move = move
        
        utilities[move] = utility
      
      self.best_move = current_best_move
      
      
        




  def max_value(self, board, alpha, beta, depth_limit):
    # Check if time limit exceeded
    self.time_out()

    # Verify if terminal state or depth limit reached or time limit
    terminal, _, _ = check_endgame(board)

    if terminal or depth_limit <= 0:
      return self.get_utility(board)
    
    # Get valid moves and reorder by quick evaluation
    valid_moves = get_valid_moves(board, self.player)
    if not valid_moves:
      return self.min_value(board, alpha, beta, depth_limit)
    valid_moves = self.order_moves(board, valid_moves, self.player)
    valid_moves = valid_moves[:self.branching_factor]

    for move in valid_moves:
      simulated_board = board.copy()
      execute_move(simulated_board, move, self.player)
      alpha = max(alpha, self.min_value(simulated_board, alpha, beta, depth_limit - 1))
      if alpha >= beta:
        return beta
    
    return alpha




  def min_value(self, board, alpha, beta, depth_limit):
    # Check if time limit exceeded
    self.time_out()

    # Verify if terminal state or depth limit reached or time limit
    terminal, _, _ = check_endgame(board)

    if terminal or depth_limit <= 0:
      return self.get_utility(board)
    
    # Get valid moves and reorder by quick evaluation
    valid_moves = get_valid_moves(board, self.opponent)
    if not valid_moves:
      return self.max_value(board, alpha, beta, depth_limit)
    valid_moves = self.order_moves(board, valid_moves, self.opponent)
    valid_moves = valid_moves[:self.branching_factor]

    for move in valid_moves:
      simulated_board = board.copy()
      execute_move(simulated_board, move, self.opponent)
      beta = min(beta, self.max_value(simulated_board, alpha, beta, depth_limit - 1))
      if alpha >= beta:
        return alpha
      
    return beta
  

  def time_out(self):
    if time.time() - self.start_time > self.time_limit:
      raise self.TimeoutException


  def order_moves(self, board, moves, player):
    return sorted(moves, key = lambda x: count_disc_count_change(board,x, player), reverse = True)




  def get_utility(self, board):
    _, p1_score, p2_score = check_endgame(board)
    if self.player == 1:
      return p1_score - p2_score
    else:
      return p2_score - p1_score
    