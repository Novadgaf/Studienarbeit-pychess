from chessboard import Chessboard
from moveGenerator import MoveGenerator
from move import Move
import random
import time

figure_values = {
    "p": 100,
    "n": 300,
    "b": 300,
    "r": 500,
    "q": 900,
    "k": 0
}

endgame_material_start = figure_values["r"] * 2 + figure_values["b"] + figure_values["n"]

class Computer:
    def __init__(self, chessboard, color) -> None:
        self.chessboard: Chessboard = chessboard
        self.move_generator = MoveGenerator(self.chessboard)
        self.color = color
        

    def choose_computer_move(self) -> Move:
        start_time = time.perf_counter()
        self.total_positions = 0
        alpha = -float("inf")
        beta = float("inf")
        #moves = self.order_moves(moves)
        self.get_moves_time = 0
        best_eval, best_move = self.minimax(3, alpha, beta, False)

        end_time = time.perf_counter()
        print(f"chose move {best_move.START_SQUARE} to {best_move.END_SQUARE} with an evaluation of {best_eval}")
        print(f"i went through {self.total_positions} total positions and it took me about {start_time-end_time:0.4f} seconds")
        print(f"getting valid moves took me abouyt {self.get_moves_time}")
        return best_move
    

    def endgame_weight(self, material_counter):
        tmp = endgame_material_start
        multiplier = 1 / tmp
        return 1 - min(1, material_counter * multiplier)
    
    def endgame_evaluation(self, color):
        score = 0
        position = self.chessboard.squares
        if color == 0b0:
            self_material, enemy_material = self.count_material()
            self_king_square = self.move_generator.find_king_square(position, color=0b0)
            enemy_king_square = self.move_generator.find_king_square(position, color=0b1)
        else:
            enemy_material, self_material = self.count_material()
            enemy_king_square = self.move_generator.find_king_square(position, color=0b0)
            self_king_square = self.move_generator.find_king_square(position, color=0b1)

        endgame_weight = self.endgame_weight(self_material)
        enemy_king_rank = enemy_king_square % 8
        enemy_king_dist_center_rank = max(3-enemy_king_rank, enemy_king_rank-4)
        enemy_king_file = int(enemy_king_square / 8)
        enemy_king_dist_center_file = max(3-enemy_king_file, enemy_king_file-4)
        
        self_king_rank = self_king_square % 8
        self_king_file = int(self_king_square / 8)

        kings_distance = abs(self_king_file-enemy_king_file) + abs(self_king_rank-enemy_king_rank)

        if endgame_weight > 0 and self_material > enemy_material:
            #enemy king close to corner
            score += 10*(enemy_king_dist_center_file + enemy_king_dist_center_rank)

            #bring king up 
            score += 14-kings_distance

            return score * 10 * endgame_weight

        return 0
        


    def evaluate_position(self):
        white_material, black_material = self.count_material()
        
        white_endgame = self.endgame_evaluation(0b0)
        black_endgame = self.endgame_evaluation(0b1)

        evaluation  = white_material - black_material + white_endgame - black_endgame
        if black_endgame == 0:
            black_endgame = self.endgame_evaluation(0b1)
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
    

    def minimax(self, depth, alpha, beta, maximizingPlayer):
        self.total_positions += 1
        #print(f"position {self.total_positions}")
        tmpTimelower = time.time()
        moves = self.order_moves(self.move_generator.generateMoves())
        tmpTimeupper = time.time()
        self.get_moves_time += tmpTimeupper - tmpTimelower
        if not moves:
            if self.move_generator.check_for_checks(self.chessboard.squares) == 0:
                return 0, None
            else:
                perspective = 1 if self.chessboard.color_to_move == 0b1 else -1
                return float('inf') * perspective, None

        if depth == 0:
            return self.evaluate_position(), None

        best_move = None
        if maximizingPlayer:
            max_evaluation = -float('inf')
            for move in moves:
                self.chessboard.make_move(move)
                eval, _ = self.minimax(depth-1, alpha, beta, False)
                self.chessboard.restore_state()
                if eval > max_evaluation:
                    max_evaluation = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_evaluation, best_move
        
        else:
            min_evaluation = float('inf')
            for move in moves:
                self.chessboard.make_move(move)
                eval, _ = self.minimax(depth-1, alpha, beta, True)
                self.chessboard.restore_state()
                if eval < min_evaluation:
                    min_evaluation = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_evaluation, best_move
    
    def order_moves(self, moves: list[Move]):
        scores = []
        for move in moves:
            move_score_guess = 0
            move_piece_type = move.FIGURE.TYPE
            capture_piece = self.chessboard.squares[move.END_SQUARE]

            if capture_piece:
                if move.END_SQUARE in self.move_generator.get_attacked_squares(capture_piece.COLOR):
                    move_score_guess = 10 * (figure_values[capture_piece.TYPE] - figure_values[move_piece_type])
                else:
                    move_score_guess = 10*figure_values[capture_piece.TYPE]
            
            self.chessboard.make_move(move)
            checks = self.move_generator.check_for_checks(self.chessboard.squares)
            if  checks > 0:
                move_score_guess += checks*10
            self.chessboard.restore_state()
            scores.append(move_score_guess)

        self.sort(scores, moves)

        return moves
         
    def quick_sort(self, scores, moves, low, high):
        if low < high:
            pivot_index = self.partition(scores, moves, low, high)
            self.quick_sort(scores, moves, low, pivot_index - 1)
            self.quick_sort(scores, moves, pivot_index + 1, high)

    def partition(self, scores, moves, low, high):
        pivot = scores[high]
        i = low - 1

        for j in range(low, high):
            if scores[j] >= pivot:
                i += 1
                scores[i], scores[j] = scores[j], scores[i]
                moves[i], moves[j] = moves[j], moves[i]

        scores[i + 1], scores[high] = scores[high], scores[i + 1]
        moves[i + 1], moves[high] = moves[high], moves[i + 1]
        return i + 1

    def sort(self, scores, moves):
        self.quick_sort(scores, moves, 0, len(scores) - 1)
        return moves