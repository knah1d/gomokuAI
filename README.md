# Gomoku AI

A Gomoku (Five-in-a-row) game with an AI opponent powered by the minimax algorithm with alpha-beta pruning.

## Features

- Play against an AI on a 10×10 Gomoku board
- AI uses minimax algorithm with alpha-beta pruning
- Custom evaluation function to score board states
- Graphical user interface built with Tkinter
- AI has early stopping based on time limit

## Requirements

- Python 3.x
- NumPy

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/gomokuAI.git
cd gomokuAI
```

2. Install the required packages:
```
pip install -r requirements.txt
```

## How to Play

Run the main.py file to start the game:
```
python main.py
```

- Click on the board to place your stone (black)
- The AI will respond with its move (white)
- The first player to form an unbroken chain of 5 stones in a row (horizontally, vertically, or diagonally) wins

## Project Structure

- `main.py`: Entry point for the game
- `gomoku_game.py`: Core game logic
- `gomoku_ai.py`: AI implementation with minimax and alpha-beta pruning
- `gomoku_gui.py`: Graphical user interface
- `requirements.txt`: List of dependencies

## AI Implementation Details

- **Minimax Algorithm**: Explores possible future game states to find the optimal move
- **Alpha-Beta Pruning**: Optimizes the search by skipping branches that won't affect the final decision
- **Evaluation Function**: Scores intermediate board states by analyzing patterns like open/closed rows
- **Early Stopping**: Limits computation time to ensure responsive gameplay
- **Move Ordering**: Prioritizes more promising moves to improve pruning efficiency
- **Transposition Table**: Caches previously evaluated positions to avoid redundant calculations 