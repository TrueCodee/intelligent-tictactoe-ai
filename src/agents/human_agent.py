class HumanAgent:
    def __init__(self, mark):
        """
        Initialize a human player.
        
        Args:
            mark (str): The player's mark ('X' or 'O')
        """
        self.mark = mark
    
    def get_move(self, board):
        """
        Get a move from the human player.
        
        Args:
            board: The game board
            
        Returns:
            tuple: (row, col) representing the player's move
        """
        valid_moves = board.get_valid_moves()
        
        while True:
            try:
                row = int(input(f"Player {self.mark}, enter row (0-{board.size-1}): "))
                col = int(input(f"Player {self.mark}, enter col (0-{board.size-1}): "))
                
                if (row, col) in valid_moves:
                    return (row, col)
                else:
                    print(f"Invalid move! Choose from available moves: {valid_moves}")
            except ValueError:
                print("Please enter valid numbers.")