import stockfish
from figures import *

from chessboard import Chessboard, square_name_to_index
from moveGenerator import MoveGenerator

class Bot:
    def __init__(self, chessboard: Chessboard, color, stockfish_path) -> None:    
        self.fisher = stockfish.Stockfish(stockfish_path)
        self.fisher.set_elo_rating(2000)
        self.chessboard = chessboard
        self.move_generator = MoveGenerator(self.chessboard)
        self.color = color
        
    def get_move(self):
        fen = self.chessboard.generate_fen_from_current_position()
        if not self.fisher.is_fen_valid(fen):
            print("Wrong fen generated")
            return None
        self.fisher.set_fen_position(fen)
        dict = self.fisher.get_evaluation()
        print(dict)
        bot_move = self.fisher.get_best_move_time(1000)
        valid_moves = self.move_generator.generateMoves()
        print(bot_move)
        start_square = square_name_to_index(bot_move[:2])
        end_square = square_name_to_index(bot_move[2:])
        for move in valid_moves:
            if  start_square == move.START_SQUARE and end_square == move.END_SQUARE:
                if move.IS_PROMOTION:
                    promotion_piece_type = bot_move[4]
                    if promotion_piece_type.lower() == "q":
                        promotion_piece = Queen(self.color)
                    elif promotion_piece_type.lower() == "r":
                        promotion_piece = Rook(self.color)
                    elif promotion_piece_type.lower() == "n":
                        promotion_piece = Knight(self.color)
                    elif promotion_piece_type.lower() == "b":
                        promotion_piece = Bishop(self.color)

                    move.set_promotion_piece(promotion_piece)
                return move
            
        print(f"playing random move {move.START_SQUARE} to {move.END_SQUARE}")
        return move
    