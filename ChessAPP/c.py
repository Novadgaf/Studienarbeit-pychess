from chessboard import Chessboard
from moveGenerator import MoveGenerator
from move import Move
import random

figure_values = {
    "p": 1,
    "n": 3,
    "b": 3,
    "r": 5,
    "q": 9,
    "k": 0
}

class Computefr:
    def __init__(self, chessboard, color) -> None:
        self.chessboard: Chessboard = chessboard
        self.move_generator = MoveGenerator(self.chessboard)
        self.color = color

    def choose_computer_move(self) -> Move:
        best_move = None
        best_eval = 0
        alpha = -5
        beta = 5
        moves = self.order_moves(self.move_generator.generateMoves())
        for x, move in enumerate(moves):
            print(f"\n\n\nmove {x} from {len(moves)}")
            print(f"trying outcome for move {move.START_SQUARE} to {move.END_SQUARE}")
            self.chessboard.make_move(move)
            
            move_evaluation = self.search(1, alpha, beta)
            if  move_evaluation > best_eval:
                print(f"\n\n\nbetter evaluation found {move.START_SQUARE} to {move.END_SQUARE}\n\n\n")
                best_eval = move_evaluation
                best_move = move
            self.chessboard.restore_state()
        
        return best_move
    
    def evaluate_position(self):
        whiteEval, blackEval = self.count_material()
        perspective = 1 if self.chessboard.color_to_move == self.color else -1
        evaluation  = (whiteEval - blackEval) * perspective

        return evaluation
      

    def count_material(self):
        white_material = 0
        black_material = 0

        for figure in self.chessboard.squares:
            if figure is None: 
                continue
            
            points = figure_values[figure.TYPE]

            if figure.COLOR == 0b0:
                white_material += points
            else:
                black_material += points
        
        return (white_material, black_material)
    

    def search(self, depth, alpha, beta):
        print("white" if self.chessboard.color_to_move == 0b0 else 'black')
        moves = self.move_generator.generateMoves()
        if not moves:
            return -float('inf')
        
        if depth == 0:
            return self.evaluate_position()

        moves = self.order_moves(moves)

        for move in moves:
            self.chessboard.make_move(move)
            evaluation = -self.search(depth-1, -beta, -alpha)
            self.chessboard.restore_state()
            print(f"move {move.START_SQUARE} to {move.END_SQUARE} evaluation is {evaluation}")
            if evaluation >= beta:
                print(f"returning beta with {beta}")
                return beta
            print(f"new alpha is max of alpha {alpha} beta {evaluation}")
            alpha = max(alpha, evaluation)
        print(f"returning alpha with {alpha}")
        return alpha


    def order_moves(self, moves: list[Move]):
        scores = []
        for move in moves:
            move_score_guess = 0
            move_piece_type = move.FIGURE.TYPE
            capture_piece = self.chessboard.squares[move.END_SQUARE]

            if capture_piece:
                move_score_guess = 10 * (figure_values[capture_piece.TYPE] - figure_values[move_piece_type])

            pawn_attacked_squares = self.move_generator.get_attacked_squares(self.chessboard.color_to_move, "p")
            if move.END_SQUARE in pawn_attacked_squares:
                move_score_guess -= figure_values[move_piece_type]

            scores.append(move_score_guess)

        #print(f"\n\n\n\n\n\nlen moves: {len(moves)}\nlen scores: {len(scores)}\n\n\n\n\n\n")
        self.sort(scores, moves)

        return moves

            
    def quick_sort(self, scores, moves, low, high):
        if low < high:
            pivot_index = self.partition(scores, moves, low, high)
            if pivot_index > 0:  # Add this condition to prevent infinite recursion
                self.quick_sort(scores, moves, low, pivot_index - 1)  # Change this line
            self.quick_sort(scores, moves, pivot_index + 1, high)


    def partition(self, scores, moves, low, high):
        pivot = scores[low]
        left = low + 1
        right = high

        done = False
        while not done:
            while left <= right and scores[left] <= pivot:
                left = left + 1
            while scores[right] >= pivot and right >= left:
                right = right - 1
            if right < left:
                done = True
            else:
                scores[left], scores[right] = scores[right], scores[left]
                moves[left], moves[right] = moves[right], moves[left]
        
        scores[low], scores[right] = scores[right], scores[low]
        moves[low], moves[right] = moves[right], moves[low]
        
        return right


    def sort(self, scores, moves):
        self.quick_sort(scores, moves, 0, len(scores) - 1)
