import time
import math
import random
import copy

EMPTY = ' '
HUMAN = 'O'
AI = 'X'


class TicTacToe:
    def __init__(self):
        self.board = [EMPTY] * 9

    def print_board(self):
        for i in range(3):
            print('|'.join(self.board[i*3:(i+1)*3]))
            if i < 2:
                print('-----')

    def available_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == EMPTY]

    def make_move(self, position, player):
        if self.board[position] == EMPTY:
            self.board[position] = player
            return True
        return False

    def is_winner(self, player):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        return any(all(self.board[i] == player for i in combo) for combo in wins)

    def is_draw(self):
        return EMPTY not in self.board and not self.is_winner(HUMAN) and not self.is_winner(AI)

    def game_over(self):
        return self.is_winner(HUMAN) or self.is_winner(AI) or self.is_draw()

    def reset(self):
        self.board = [EMPTY] * 9


# -----------------------
# Minimax Algorithm
# -----------------------
def minimax(board, depth, is_maximizing):
    if board.is_winner(AI):
        return 10 - depth
    if board.is_winner(HUMAN):
        return depth - 10
    if board.is_draw():
        return 0

    if is_maximizing:
        best = -math.inf
        for move in board.available_moves():
            board.make_move(move, AI)
            score = minimax(board, depth + 1, False)
            board.board[move] = EMPTY
            best = max(score, best)
        return best
    else:
        best = math.inf
        for move in board.available_moves():
            board.make_move(move, HUMAN)
            score = minimax(board, depth + 1, True)
            board.board[move] = EMPTY
            best = min(score, best)
        return best


# -----------------------
# Alpha-Beta Pruning
# -----------------------
def alphabeta(board, depth, alpha, beta, is_maximizing):
    if board.is_winner(AI):
        return 10 - depth
    if board.is_winner(HUMAN):
        return depth - 10
    if board.is_draw():
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for move in board.available_moves():
            board.make_move(move, AI)
            eval = alphabeta(board, depth + 1, alpha, beta, False)
            board.board[move] = EMPTY
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in board.available_moves():
            board.make_move(move, HUMAN)
            eval = alphabeta(board, depth + 1, alpha, beta, True)
            board.board[move] = EMPTY
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


# -----------------------
# AI Move Selection
# -----------------------
def get_best_move(board, use_ab_pruning=False):
    best_score = -math.inf
    best_move = None

    for move in board.available_moves():
        board.make_move(move, AI)
        if use_ab_pruning:
            score = alphabeta(board, 0, -math.inf, math.inf, False)
        else:
            score = minimax(board, 0, False)
        board.board[move] = EMPTY

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


# -----------------------
# Performance Comparison
# -----------------------
def compare_performance():
    board = TicTacToe()
    test_runs = 5
    results = {"minimax": 0.0, "alphabeta": 0.0}

    for _ in range(test_runs):
        b1 = copy.deepcopy(board)
        start = time.time()
        get_best_move(b1, use_ab_pruning=False)
        results["minimax"] += time.time() - start

        b2 = copy.deepcopy(board)
        start = time.time()
        get_best_move(b2, use_ab_pruning=True)
        results["alphabeta"] += time.time() - start

    print("\n⏱ Performance Comparison (avg over {} runs):".format(test_runs))
    print(f"Minimax: {results['minimax'] / test_runs:.6f} seconds")
    print(f"Alpha-Beta: {results['alphabeta'] / test_runs:.6f} seconds")


# -----------------------
# Run Demo
# -----------------------
if __name__ == "__main__":
    game = TicTacToe()
    print("Initial Board:")
    game.print_board()

    # Run one move using both
    print("\nAI's best move using Minimax:")
    best = get_best_move(game, use_ab_pruning=False)
    print("Best move:", best)

    print("\nAI's best move using Alpha-Beta:")
    best = get_best_move(game, use_ab_pruning=True)
    print("Best move:", best)

    compare_performance()