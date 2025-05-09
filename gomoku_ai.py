"""
Gomoku AI Implementation

This module implements an AI for the Gomoku game using the minimax algorithm
with alpha-beta pruning and a custom evaluation function.
"""

import numpy as np
import time

class GomokuAI:
    """
    AI player for Gomoku using minimax with alpha-beta pruning.
    """
    
    def __init__(self, max_depth=5, time_limit=2, player_id=2):
        """
        Initialize the AI with specified parameters.
        
        Args:
            max_depth: Maximum search depth
            time_limit: Maximum time (in seconds) to search
            player_id: Player ID for the AI (usually 2 for white)
        """
        self.max_depth = max_depth
        self.time_limit = time_limit
        self.player_id = player_id  # AI player (usually 2)
        self.opponent_id = 3 - player_id  # Human player (usually 1)
        self.start_time = 0
        self.nodes_evaluated = 0
        self.transposition_table = {}  # For storing evaluated positions
    
    def choose_move(self, game):
        """
        Choose the best move for the current game state.
        
        Args:
            game: Current GomokuGame instance
            
        Returns:
            tuple: (row, col) of the best move
        """
        self.start_time = time.time()
        self.nodes_evaluated = 0
        self.transposition_table = {}
        
        # Get valid moves
        valid_moves = self.get_sorted_moves(game)
        
        if not valid_moves:
            return None
            
        # If this is the first move, just play in the center
        if np.count_nonzero(game.board) == 0:
            return (game.board_size // 2, game.board_size // 2)
        
        # If this is the second move, play adjacent to the first move
        if np.count_nonzero(game.board) == 1:
            row, col = np.nonzero(game.board)
            row, col = row[0], col[0]
            # Choose a position adjacent to the opponent's move
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    new_r, new_c = row + dr, col + dc
                    if game.is_valid_move(new_r, new_c):
                        return (new_r, new_c)
        
        # Use iterative deepening to find the best move within time limit
        best_move = valid_moves[0]  # Default to first valid move
        
        for depth in range(1, self.max_depth + 1):
            if time.time() - self.start_time > self.time_limit:
                break
                
            best_score = float('-inf')
            alpha = float('-inf')
            beta = float('inf')
            
            for move in valid_moves:
                row, col = move
                # Make the move
                game.board[row, col] = self.player_id
                
                # Evaluate this move
                score = self.minimax(game, depth - 1, alpha, beta, False)
                
                # Undo the move
                game.board[row, col] = 0
                
                if score > best_score:
                    best_score = score
                    best_move = move
                
                alpha = max(alpha, best_score)
                
                # Check time limit
                if time.time() - self.start_time > self.time_limit:
                    break
        
        print(f"AI evaluated {self.nodes_evaluated} nodes in {time.time() - self.start_time:.2f} seconds")
        return best_move
    
    def minimax(self, game, depth, alpha, beta, is_maximizing):
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            game: Current game state
            depth: Current search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            is_maximizing: True if maximizing player's turn
            
        Returns:
            float: Score of the best move
        """
        self.nodes_evaluated += 1
        
        # Check if time limit is exceeded
        if time.time() - self.start_time > self.time_limit:
            # Return a score based on the current state
            return self.evaluate(game)
        
        # Create a hash of the current board state + player info
        board_hash = hash((game.board.tobytes(), is_maximizing))
        
        # Check if we've already evaluated this position
        if board_hash in self.transposition_table and depth <= self.transposition_table[board_hash]['depth']:
            return self.transposition_table[board_hash]['score']
        
        # Check for terminal states (win/loss/draw)
        winner = self.check_winner(game)
        if winner == self.player_id:  # AI wins
            return 1000000
        elif winner == self.opponent_id:  # Human wins
            return -1000000
        elif len(game.get_valid_moves()) == 0:  # Draw
            return 0
        
        # If we've reached the maximum depth, evaluate the position
        if depth == 0:
            score = self.evaluate(game)
            self.transposition_table[board_hash] = {'score': score, 'depth': depth}
            return score
        
        sorted_moves = self.get_sorted_moves(game)
        
        if is_maximizing:  # AI's turn
            max_score = float('-inf')
            for move in sorted_moves:
                row, col = move
                game.board[row, col] = self.player_id
                
                score = self.minimax(game, depth - 1, alpha, beta, False)
                
                game.board[row, col] = 0  # Undo move
                
                max_score = max(max_score, score)
                alpha = max(alpha, max_score)
                
                if beta <= alpha:
                    break  # Beta cutoff
            
            self.transposition_table[board_hash] = {'score': max_score, 'depth': depth}
            return max_score
        
        else:  # Opponent's turn
            min_score = float('inf')
            for move in sorted_moves:
                row, col = move
                game.board[row, col] = self.opponent_id
                
                score = self.minimax(game, depth - 1, alpha, beta, True)
                
                game.board[row, col] = 0  # Undo move
                
                min_score = min(min_score, score)
                beta = min(beta, min_score)
                
                if beta <= alpha:
                    break  # Alpha cutoff
            
            self.transposition_table[board_hash] = {'score': min_score, 'depth': depth}
            return min_score
    
    def get_sorted_moves(self, game):
        """
        Get valid moves sorted by their potential (proximity to existing stones).
        This improves pruning efficiency by trying more promising moves first.
        """
        valid_positions = []
        
        # Only consider moves that are adjacent to existing stones
        # This focuses the search on more promising areas
        for r in range(game.board_size):
            for c in range(game.board_size):
                if game.board[r, c] == 0:  # Empty cell
                    # Check if any adjacent cell has a stone
                    has_neighbor = False
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            nr, nc = r + dr, c + dc
                            if (0 <= nr < game.board_size and 
                                0 <= nc < game.board_size and 
                                game.board[nr, nc] != 0):
                                has_neighbor = True
                                break
                        if has_neighbor:
                            break
                    
                    if has_neighbor or np.count_nonzero(game.board) < 2:
                        # Calculate a heuristic value for this move
                        game.board[r, c] = self.player_id
                        ai_score = self.evaluate_position(game, r, c, self.player_id)
                        game.board[r, c] = self.opponent_id
                        human_score = self.evaluate_position(game, r, c, self.opponent_id)
                        game.board[r, c] = 0  # Reset
                        
                        # Prioritize defense slightly more (prevent opponent wins)
                        score = max(ai_score, human_score * 1.1)
                        valid_positions.append(((r, c), score))
        
        # If no moves with neighbors, consider all empty cells
        if not valid_positions and np.count_nonzero(game.board) > 0:
            for r in range(game.board_size):
                for c in range(game.board_size):
                    if game.board[r, c] == 0:
                        valid_positions.append(((r, c), 0))
        
        # Sort by score (descending)
        valid_positions.sort(key=lambda x: x[1], reverse=True)
        return [pos for pos, _ in valid_positions]
    
    def check_winner(self, game):
        """Check if there's a winner in the current board state."""
        board = game.board
        
        # Check horizontal, vertical, and diagonal wins
        directions = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],  # Vertical
            [(1, 1), (-1, -1)],  # Diagonal \
            [(1, -1), (-1, 1)]   # Diagonal /
        ]
        
        for r in range(game.board_size):
            for c in range(game.board_size):
                if board[r, c] != 0:  # If there's a stone here
                    player = board[r, c]
                    
                    for dir_pair in directions:
                        count = 1  # Count the stone at (r, c)
                        
                        # Check in both directions
                        for dr, dc in dir_pair:
                            row, col = r, c
                            for _ in range(4):  # Need 5 in a row to win
                                row, col = row + dr, col + dc
                                if (0 <= row < game.board_size and 
                                    0 <= col < game.board_size and 
                                    board[row, col] == player):
                                    count += 1
                                else:
                                    break
                        
                        if count >= 5:
                            return player
        
        return None
    
    def evaluate(self, game):
        """
        Evaluate the current board state from the AI's perspective.
        
        Returns:
            float: Score of the board state (higher is better for AI)
        """
        board = game.board
        ai_score = 0
        human_score = 0
        
        # Check for patterns in all directions
        for r in range(game.board_size):
            for c in range(game.board_size):
                if board[r, c] == self.player_id:
                    ai_score += self.evaluate_position(game, r, c, self.player_id)
                elif board[r, c] == self.opponent_id:
                    human_score += self.evaluate_position(game, r, c, self.opponent_id)
        
        return ai_score - human_score
    
    def evaluate_position(self, game, row, col, player_id):
        """
        Evaluate a position for a specific player.
        Checks for patterns like open/closed runs of stones.
        
        Args:
            game: Current game state
            row, col: Position to evaluate
            player_id: Player to evaluate for
            
        Returns:
            float: Score for this position
        """
        board = game.board
        opponent_id = 3 - player_id
        score = 0
        
        # Patterns to check (open runs are worth more than blocked runs)
        # Format: [pattern, score]
        patterns = {
            # Five in a row (win)
            "FIVE": 100000,
            # Open four (one stone away from winning with two ways to win)
            "OPEN_FOUR": 10000,
            # Closed four (one stone away but can be blocked)
            "CLOSED_FOUR": 1000,
            # Open three (two stones away with multiple ways to create an open four)
            "OPEN_THREE": 500,
            # Closed three (two stones away but more restricted)
            "CLOSED_THREE": 100,
            # Open two (three stones away but with potential)
            "OPEN_TWO": 50,
            # Closed two (three stones away and restricted)
            "CLOSED_TWO": 10
        }
        
        directions = [
            (1, 0),   # Vertical
            (0, 1),   # Horizontal
            (1, 1),   # Diagonal \
            (1, -1)   # Diagonal /
        ]
        
        for dr, dc in directions:
            # Look for patterns in both directions from the stone
            line = []
            for i in range(-5, 6):  # Check 11 positions (5 in each direction + the stone itself)
                r, c = row + dr * i, col + dc * i
                if 0 <= r < game.board_size and 0 <= c < game.board_size:
                    if board[r, c] == player_id:
                        line.append("X")  # Player's stone
                    elif board[r, c] == opponent_id:
                        line.append("O")  # Opponent's stone
                    else:
                        line.append(".")  # Empty
                else:
                    line.append("B")  # Boundary
            
            line_str = "".join(line)
            
            # Check for five in a row
            if "XXXXX" in line_str:
                score += patterns["FIVE"]
            
            # Check for open four
            if ".XXXX." in line_str:
                score += patterns["OPEN_FOUR"]
            
            # Check for closed four (blocked on one side)
            if "OXXXX." in line_str or ".XXXXO" in line_str or "BXXXX." in line_str or ".XXXXB" in line_str:
                score += patterns["CLOSED_FOUR"]
            
            # Check for open three
            if ".XXX.." in line_str or "..XXX." in line_str:
                score += patterns["OPEN_THREE"]
            
            # Check for closed three
            if "OXXX.." in line_str or "..XXXO" in line_str or "BXXX.." in line_str or "..XXXB" in line_str:
                score += patterns["CLOSED_THREE"]
            
            # Check for open two
            if ".XX..." in line_str or "...XX." in line_str:
                score += patterns["OPEN_TWO"]
            
            # Check for closed two
            if "OXX..." in line_str or "...XXO" in line_str or "BXX..." in line_str or "...XXB" in line_str:
                score += patterns["CLOSED_TWO"]
        
        return score 