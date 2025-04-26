class ConsoleView:
    def __init__(self):
        """Initialize console view for the game."""
        pass
    
    def display_board(self, board):
        """
        Display the board in the console.
        
        Args:
            board: The game board
        """
        print("\n" + str(board))
    
    def display_move(self, mark, row, col):
        """
        Display a move in the console.
        
        Args:
            mark (str): The player's mark
            row (int): Row index
            col (int): Column index
        """
        print(f"Player {mark} placed at position ({row}, {col})")
    
    def display_winner(self, mark):
        """
        Display the winner in the console.
        
        Args:
            mark (str): The winner's mark
        """
        print(f"\n***** Player {mark} wins! *****\n")
    
    def display_draw(self):
        """Display a draw in the console."""
        print("\n***** Game ended in a draw *****\n")