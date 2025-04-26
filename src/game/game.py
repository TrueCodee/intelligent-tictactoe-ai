import time
from game.board import Board

class TicTacToe:
    def __init__(self, board_size=3, agent1=None, agent2=None, view=None, metrics=None, tree_viz=None, quiet=False):
        """
        Initialize the Tic-Tac-Toe game.
        
        Args:
            board_size (int): Size of the board (3 for 3x3, 5 for 5x5)
            agent1: First player (X)
            agent2: Second player (O)
            view: Visualization component
            metrics: Metrics collector
            tree_viz: Tree visualizer (optional)
            quiet (bool): If True, minimal output will be shown
        """
        self.board = Board(board_size)
        self.agent1 = agent1  # AI or human for X
        self.agent2 = agent2  # AI or human for O
        self.view = view
        self.metrics = metrics
        self.tree_viz = tree_viz
        self.quiet = quiet
        
        # Track current player as 'X' or 'O'
        self.current_player = 'X'
    
    def switch_player(self):
        """Switch the current player between 'X' and 'O'."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def get_current_agent(self):
        """
        Get the agent corresponding to the current player.

        Returns:
            Agent object (if AI) or None (if human)
        """
        return self.agent1 if self.current_player == 'X' else self.agent2

    def play(self):
        """
        Play the game until completion.
        
        Returns:
            str or None: The mark of the winner ('X' or 'O'), or None for a draw
        """
        if not self.quiet:
            self.view.display_board(self.board)
        
        while not self.board.is_game_over():
            # Get the agent for the current player
            current_agent = self.get_current_agent()

            if current_agent is not None:  # AI Turn
                print(f"({self.current_player})'s turn...") #to help debug
                start_time = time.time()
                move = current_agent.get_move(self.board)
                end_time = time.time()

                # Log AI move execution time
                if self.metrics:
                    agent_type = current_agent.__class__.__name__.lower().replace('agent', '')
                    self.metrics.record_move_time(agent_type, end_time - start_time)
            else:  #  Human turn (handled in GUI)
                move = None  # Let GUI handle human input

            # If AI made a move, validate and update board
            if move:
                row, col = move
                if not self.board.make_move(row, col, self.current_player):
                    if not self.quiet:
                        print(f"Invalid move by {self.current_player}!")
                    continue  # Skip to next iteration if invalid
            
                # Update the GUI or console view
                if not self.quiet:
                    self.view.display_board(self.board)
                    self.view.display_move(self.current_player, row, col)

                # Switch to the next player
                self.switch_player()
        
        #  Determine winner and display result
        winner = self.board.get_winner()
        if not self.quiet:
            if winner:
                self.view.display_winner(winner)
            else:
                self.view.display_draw()
        
        return winner