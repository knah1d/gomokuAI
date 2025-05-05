"""
Gomoku Game Logic

This module contains the core game logic for a 10x10 Gomoku game.
"""

import numpy as np

class GomokuGame:
    """
    Implements the Gomoku game logic on a 10x10 board.
    
    The game state is represented using a 2D numpy array where:
    - 0 represents an empty cell
    - 1 represents a player stone (black)
    - 2 represents an AI stone (white)
    """
    
    def __init__(self, board_size=10):
        """Initialize an empty Gomoku board."""
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype=int)
        self.current_player = 1  # Player 1 (human) starts
        self.last_move = None
        self.game_over = False
        self.winner = None
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_player = 1
        self.last_move = None
        self.game_over = False
        self.winner = None
    
    def is_valid_move(self, row, col):
        """Check if a move is valid (in bounds and cell is empty)."""
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            return self.board[row, col] == 0
        return False
    
    def make_move(self, row, col):
        """
        Make a move on the board and check for a win.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            bool: True if the move was successful, False otherwise
        """
        if not self.is_valid_move(row, col) or self.game_over:
            return False
        
        self.board[row, col] = self.current_player
        self.last_move = (row, col)
        
        # Check if this move results in a win
        if self.check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
        # Check if the board is full (draw)
        elif np.count_nonzero(self.board) == self.board_size * self.board_size:
            self.game_over = True
            self.winner = 0  # Draw
        else:
            # Switch to the other player
            self.current_player = 3 - self.current_player  # Alternates between 1 and 2
        
        return True
    
    def check_win(self, row, col):
        """Check if the last move at (row, col) resulted in 5 in a row."""
        player = self.board[row, col]
        directions = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],  # Vertical
            [(1, 1), (-1, -1)],  # Diagonal \
            [(1, -1), (-1, 1)]   # Diagonal /
        ]
        
        for dir_pair in directions:
            count = 1  # Count the stone at (row, col)
            
            # Check in both directions
            for dr, dc in dir_pair:
                r, c = row, col
                for _ in range(4):  # Need 5 in a row to win
                    r, c = r + dr, c + dc
                    if (0 <= r < self.board_size and 
                        0 <= c < self.board_size and 
                        self.board[r, c] == player):
                        count += 1
                    else:
                        break
                        
            if count >= 5:
                return True
                
        return False
    
    def get_valid_moves(self):
        """Return a list of all valid moves on the board."""
        valid_moves = []
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r, c] == 0:
                    valid_moves.append((r, c))
        return valid_moves
    
    def get_board_copy(self):
        """Return a deep copy of the current board state."""
        return self.board.copy()
    
    def get_board_state(self):
        """Return a tuple of (board, current_player, game_over, winner)."""
        return (self.board.copy(), self.current_player, 
                self.game_over, self.winner)
    
    def __str__(self):
        """String representation of the board."""
        symbols = {0: ".", 1: "X", 2: "O"}
        result = "  " + " ".join(str(i) for i in range(self.board_size)) + "\n"
        for i in range(self.board_size):
            result += f"{i} " + " ".join(symbols[self.board[i, j]] for j in range(self.board_size)) + "\n"
        return result 