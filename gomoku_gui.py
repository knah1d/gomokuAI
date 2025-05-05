"""
Gomoku Game GUI

This module implements a graphical user interface for the Gomoku game using Tkinter.
"""

import tkinter as tk
from tkinter import messagebox
import time
from gomoku_game import GomokuGame
from gomoku_ai import GomokuAI

class GomokuGUI:
    """
    GUI for the Gomoku game using Tkinter.
    """
    
    def __init__(self, root, board_size=10, cell_size=50):
        """
        Initialize the GUI.
        
        Args:
            root: Tkinter root window
            board_size: Size of the Gomoku board (default is 10)
            cell_size: Size of each cell in pixels (default is 50)
        """
        self.root = root
        self.board_size = board_size
        self.cell_size = cell_size
        
        # Set up the game logic
        self.game = GomokuGame(board_size)
        self.ai = GomokuAI(max_depth=3, time_limit=2)
        
        # Set up window properties
        self.root.title("Gomoku Game")
        self.canvas_size = board_size * cell_size
        
        # Create a frame for the board
        self.board_frame = tk.Frame(root)
        self.board_frame.pack(padx=10, pady=10)
        
        # Create the canvas for drawing the board
        self.canvas = tk.Canvas(
            self.board_frame, 
            width=self.canvas_size, 
            height=self.canvas_size, 
            bg="#E8B96F"  # Light wood color
        )
        self.canvas.pack()
        
        # Create a frame for control buttons
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(padx=10, pady=5, fill=tk.X)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Your turn (Black)")
        self.status_label = tk.Label(
            self.control_frame, 
            textvariable=self.status_var,
            font=("Arial", 12)
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Reset button
        self.reset_button = tk.Button(
            self.control_frame, 
            text="New Game", 
            command=self.reset_game,
            font=("Arial", 10)
        )
        self.reset_button.pack(side=tk.RIGHT, padx=10)
        
        # Draw the initial board
        self.draw_board()
        
        # Bind mouse click event
        self.canvas.bind("<Button-1>", self.handle_click)
        
        # Flag to prevent clicks during AI's turn
        self.waiting_for_ai = False
    
    def draw_board(self):
        """Draw the Gomoku board with grid lines and points."""
        # Clear the canvas
        self.canvas.delete("all")
        
        # Draw grid lines
        for i in range(self.board_size):
            # Horizontal lines
            self.canvas.create_line(
                0, i * self.cell_size + self.cell_size // 2,
                self.canvas_size, i * self.cell_size + self.cell_size // 2,
                width=1
            )
            # Vertical lines
            self.canvas.create_line(
                i * self.cell_size + self.cell_size // 2, 0,
                i * self.cell_size + self.cell_size // 2, self.canvas_size,
                width=1
            )
        
        # Draw star points (traditional Gomoku board has star points)
        star_points = []
        if self.board_size >= 15:  # Traditional star points for 15x15 board
            star_points = [(3, 3), (3, 7), (3, 11), (7, 3), (7, 7), (7, 11), (11, 3), (11, 7), (11, 11)]
        else:  # Simplified for 10x10 board
            mid = self.board_size // 2
            offset = 2
            star_points = [
                (mid - offset, mid - offset), 
                (mid - offset, mid + offset - 1), 
                (mid + offset - 1, mid - offset), 
                (mid + offset - 1, mid + offset - 1)
            ]
        
        for point in star_points:
            r, c = point
            x = c * self.cell_size + self.cell_size // 2
            y = r * self.cell_size + self.cell_size // 2
            self.canvas.create_oval(
                x - 3, y - 3, x + 3, y + 3,
                fill="black"
            )
        
        # Draw stones
        for r in range(self.board_size):
            for c in range(self.board_size):
                self.draw_stone(r, c)
    
    def draw_stone(self, row, col):
        """Draw a stone at the specified position."""
        if self.game.board[row, col] != 0:
            x = col * self.cell_size + self.cell_size // 2
            y = row * self.cell_size + self.cell_size // 2
            radius = int(self.cell_size * 0.4)  # Size of the stone
            
            # Colors for the stones
            if self.game.board[row, col] == 1:  # Player (black)
                color = "black"
                outline = "black"
            else:  # AI (white)
                color = "white"
                outline = "black"
            
            # Draw the stone with a subtle 3D effect
            self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                fill=color, outline=outline, width=1
            )
    
    def handle_click(self, event):
        """Handle mouse click events on the board."""
        if self.waiting_for_ai or self.game.game_over:
            return
        
        # Convert pixel coordinates to board indices
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        # Make sure we're within bounds
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            # Try to make the move
            if self.game.make_move(row, col):
                # Update the display
                self.draw_stone(row, col)
                
                # Check if the game is over
                if self.game.game_over:
                    self.show_game_result()
                    return
                
                # Switch to AI's turn
                self.waiting_for_ai = True
                self.status_var.set("AI is thinking...")
                self.root.update()  # Update the display
                
                # Use a slight delay before the AI's move
                self.root.after(100, self.ai_move)
    
    def ai_move(self):
        """Make a move for the AI."""
        # Get the AI's move
        start_time = time.time()
        row, col = self.ai.choose_move(self.game)
        elapsed = time.time() - start_time
        
        if row is not None and col is not None:
            # Make the move
            self.game.make_move(row, col)
            
            # Update the display
            self.draw_stone(row, col)
            
            # Check if the game is over
            if self.game.game_over:
                self.show_game_result()
            else:
                self.status_var.set(f"Your turn (Black) - AI took {elapsed:.2f}s")
        
        self.waiting_for_ai = False
    
    def show_game_result(self):
        """Show the game result."""
        if self.game.winner == 1:  # Player wins
            self.status_var.set("You won!")
            messagebox.showinfo("Game Over", "You won!")
        elif self.game.winner == 2:  # AI wins
            self.status_var.set("AI won!")
            messagebox.showinfo("Game Over", "AI won!")
        else:  # Draw
            self.status_var.set("It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
    
    def reset_game(self):
        """Reset the game to its initial state."""
        self.game.reset_game()
        self.draw_board()
        self.waiting_for_ai = False
        self.status_var.set("Your turn (Black)")


def main():
    """Main function to start the game."""
    root = tk.Tk()
    app = GomokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main() 