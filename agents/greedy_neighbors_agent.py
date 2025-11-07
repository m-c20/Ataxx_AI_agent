# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time
from helpers import random_move, execute_move, check_endgame, get_valid_moves

@register_agent("greedy_neighbors_agent")
class GreedyNeighborsAgent(Agent):
  """
  A class for your implementation. Feel free to use this class to
  add any helper functionalities needed for your agent.
  """

  def __init__(self):
    super(GreedyNeighborsAgent, self).__init__()
    self.name = "GreedyNeighborsAgent"

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
    # Get all legal moves for the current player
    legal_moves = get_valid_moves(board, player)

    if not legal_moves:
        return None  # No valid moves available, pass turn

    best_move = None
    best_score = float('-inf')

    for move in legal_moves:
        simulated_board = deepcopy(board)
        execute_move(simulated_board, move, player)
        move_score = self.evaluate_board(simulated_board, player, opponent)
        if move_score > best_score:
            best_score = move_score
            best_move = move

    # Some simple code to help you with timing. Consider checking
    # time_taken during your search and breaking with the best answer
    # so far when it nears 2 seconds.
    start_time = time.time()
    time_taken = time.time() - start_time

    print("My AI's turn took ", time_taken, "seconds.")

    # Returns the move allowing the maximum gain 
    return best_move

  def evaluate_board(self, board, player, opponent):
      # Evaluated board based on gained resulting score
      player_count = np.sum(board == player)
      return player_count