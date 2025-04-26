import time
import json
import os
import random
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiAgent:
    def __init__(self, mark):
        """
        Initialize the Gemini API agent.

        Args:
            mark (str): The player's mark ('X' or 'O')
        """
        self.mark = mark
        self.opponent_mark = 'O' if mark == 'X' else 'X'
        self.nodes_evaluated = 0  # For compatibility with metrics

        # Load API key from .env or fallback to config JSON
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            try:
                with open("config/gemini_config.json", "r") as f:
                    config = json.load(f)
                    api_key = config.get("GEMINI_API_KEY") or config.get("api_key")
            except (FileNotFoundError, json.JSONDecodeError):
                pass

        if not api_key:
            print("⚠️ Warning: No Gemini API key found. Using random moves instead.")
            self.api_configured = False
        else:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("gemini-1.5-pro-latest")
                self.api_configured = True
                print("✅ Gemini API initialized successfully!")
            except Exception as e:
                print(f"⚠️ Error configuring Gemini API: {e}. Using random moves instead.")
                self.api_configured = False

    def get_move(self, board):
        """
        Get the best move using the Gemini API.

        Args:
            board: The game board

        Returns:
            tuple: (row, col)
        """
        valid_moves = board.get_valid_moves()
        if len(valid_moves) == 1:
            return valid_moves[0]

        if not self.api_configured:
            return random.choice(valid_moves)

        try:
            start_time = time.time()
            board_str = self._board_to_string(board)

            prompt = f"""
            You are playing Tic-Tac-Toe as player '{self.mark}'.
            The opponent is '{self.opponent_mark}'.

            Current board ({board.size}x{board.size}):
            {board_str}

            Valid moves: {valid_moves}

            Only respond with one move from the list, using the format: row,col
            Example: 1,2
            """

            response = self.model.generate_content(prompt)
            if not response or not response.text:
                raise ValueError("Gemini API returned an empty response.")

            response_text = response.text.strip()
            row_str, col_str = response_text.split(',')
            move = (int(row_str.strip()), int(col_str.strip()))

            if move in valid_moves:
                from utils.metrics import MetricsCollector
                MetricsCollector().record_algorithm_stats('gemini', 1, time.time() - start_time)
                print(f"✅ Gemini chose move: {move}")
                return move
            else:
                print(f"⚠️ Gemini returned invalid move: {move}. Using random move instead.")
                return random.choice(valid_moves)

        except Exception as e:
            print(f"⚠️ Error using Gemini API: {e}. Using random move instead.")
            return random.choice(valid_moves)

    def _board_to_string(self, board):
        """
        Convert board to string for Gemini prompt.

        Args:
            board: The game board

        Returns:
            str: board state as a string
        """
        board_state = board.get_state()
        return "\n".join(
            "".join(cell if cell != ' ' else '-' for cell in board_state[row])
            for row in range(board.size)
        )
