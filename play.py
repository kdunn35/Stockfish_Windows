from stockfish import Stockfish
import chess

# Replace this with the full path to your Stockfish executable
STOCKFISH_PATH = r"C:\Users\Kdunn\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"

def play_game(level):
    stockfish = Stockfish(STOCKFISH_PATH)
    stockfish.set_skill_level(level)  # 0 (weak) --> 20 (strong)
    board = chess.Board()

    print("You play as Bottom (capital letters). Enter moves in UCI format (e.g., e2e4, g1f3).")

    while True:
        print("\nCurrent board:")
        print(stockfish.get_board_visual())

        # Player move
        user_input = input("Your move (or type 'quit' to restart): ")
        if user_input.lower() == "quit":
            stockfish.set_fen_position(chess.STARTING_FEN)
            return  # exit current game, return control to main()

        try:
            move = chess.Move.from_uci(user_input)
            # check for valid input
            if move in board.legal_moves:
                # your move
                board.push(move)
                stockfish.make_moves_from_current_position([user_input])
                if board.is_game_over():
                    print("Game over:", board.result())
                    stockfish.set_fen_position(chess.STARTING_FEN)
                    break

                # Stockfish move
                best_move = stockfish.get_best_move()
                print(f"Stockfish plays: {best_move}")
                stockfish.make_moves_from_current_position([best_move])
                board.push(chess.Move.from_uci(best_move))                
                if board.is_game_over():
                    print("Game over:", board.result())
                    stockfish.set_fen_position(chess.STARTING_FEN)
                    break
            else:
                print("Invalid move. Please enter a valid move.")
        except ValueError:
            print("Invalid move format. Use UCI format like 'e2e4'.")


def main():
    while True:
        # ask for skill level
        while True:
            try:
                level = int(input("Choose Stockfish skill level (0-20): "))
                if 0 <= level <= 20:
                    break
                else:
                    print("Please enter a number between 0 and 20.")
            except ValueError:
                print("Invalid input. Enter an integer between 0 and 20.")

        play_game(level)
        choice = input("Do you want to play again? (y/n): ")
        if choice.lower() != "y":
            break
    print("Goodbye!")


if __name__ == "__main__":
    main()
