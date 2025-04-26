import numpy as np

class Board:
    def __init__(self, size=3):
        """
        Initialize a Tic-Tac-Toe board.
        
        Args:
            size (int): The size of the board (default: 3 for 3x3)
        """
        self.size = size
        self.board = np.full((size, size), ' ')
        self.win_length = 3 if size == 3 else 5  # Win condition length (3-in-a-row for 3x3, 5-in-a-row for 5x5)
        
        # Track move history for visualization purposes
        self.move_history = []
        self.move_count = 0  # Track number of moves to determine the current player

    def make_move(self, row, col, mark):
        """
        Make a move on the board.
        
        Args:
            row (int): Row index
            col (int): Column index
            mark (str): Player's mark ('X' or 'O')
            
        Returns:
            bool: True if the move was valid, False otherwise
        """
        if not self.is_valid_move(row, col):
            return False
        
        self.board[row, col] = mark
        self.move_history.append((row, col, mark))
        self.move_count += 1  # Increment move count
        return True

    def is_valid_move(self, row, col):
        """
        Check if a move is valid.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            bool: True if the move is valid, False otherwise
        """
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row, col] == ' '

    def get_valid_moves(self):
        """
        Get all valid moves on the board.
        
        Returns:
            list: List of (row, col) tuples representing valid moves
        """
        return [(row, col) for row in range(self.size) for col in range(self.size) if self.is_valid_move(row, col)]

    def is_full(self):
        """
        Check if the board is full.
        
        Returns:
            bool: True if the board is full, False otherwise
        """
        return len(self.get_valid_moves()) == 0

    def check_win(self, mark):
        """
        Check if a player has won.
        
        Args:
            mark (str): Player's mark ('X' or 'O')
            
        Returns:
            bool: True if the player has won, False otherwise
        """
        # print (f"Checking win for {mark}")
        # Check rows
        for row in range(self.size):
            for col in range(self.size - self.win_length + 1):
                if all(self.board[row, col+i] == mark for i in range(self.win_length)):
                    return True

        # Check columns
        for col in range(self.size):
            for row in range(self.size - self.win_length + 1):
                if all(self.board[row+i, col] == mark for i in range(self.win_length)):
                    return True

        # Check diagonals (down-right)
        for row in range(self.size - self.win_length + 1):
            for col in range(self.size - self.win_length + 1):
                if all(self.board[row+i, col+i] == mark for i in range(self.win_length)):
                    return True

        # Check diagonals (up-right)
        for row in range(self.win_length - 1, self.size):
            for col in range(self.size - self.win_length + 1):
                if all(self.board[row-i, col+i] == mark for i in range(self.win_length)):
                    return True

        return False

    def get_winner(self):
        """
        Get the winner of the game, if any.
        
        Returns:
            str or None: 'X' if X has won, 'O' if O has won, None if there's no winner
        """
        if self.check_win('X'):
            return 'X'
        elif self.check_win('O'):
            return 'O'
        else:
            return None

    def is_game_over(self):
        """
        Check if the game is over (either a player has won or the board is full).
        
        Returns:
            bool: True if the game is over, False otherwise
        """
        return self.get_winner() is not None or self.is_full()

    def get_state(self):
        """
        Get the current state of the board.
        
        Returns:
            numpy.ndarray: The board state
        """
        return self.board.copy()

    def get_current_player(self):
        """
        Determine the current player based on move count.

        Returns:
            str: 'X' or 'O' depending on the turn.
        """
        return 'X' if self.move_count % 2 == 0 else 'O'

    def __str__(self):
        """
        String representation of the board.
        
        Returns:
            str: String representation of the board
        """
        s = ""
        for row in range(self.size):
            s += "|"
            for col in range(self.size):
                s += f" {self.board[row, col]} |"
            s += "\n"
            if row < self.size - 1:
                s += "-" * (self.size * 4 + 1) + "\n"
        return s