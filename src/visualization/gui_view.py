import pygame
import time
import sys

class GUIView:
    def __init__(self, game):
        """Initialize GUI view for the game."""
        # Initialize pygame
        pygame.init()

        # Game instance
        self.game = game
        
        # Set up the display
        self.cell_size = 100
        self.width = 600
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tic-Tac-Toe")

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (200, 200, 200)

        # Font
        self.font = pygame.font.SysFont(None, 40)

        # Current board size
        self.board_size = game.board.size

    def display_board(self):
        """Display the board using pygame and keep the game responsive."""
        self.cell_size = min(self.width, self.height) // self.board_size
        self.screen.fill(self.WHITE)

        # Draw grid lines
        for i in range(1, self.board_size):
            pygame.draw.line(self.screen, self.BLACK, (i * self.cell_size, 0), (i * self.cell_size, self.board_size * self.cell_size), 2)
            pygame.draw.line(self.screen, self.BLACK, (0, i * self.cell_size), (self.board_size * self.cell_size, i * self.cell_size), 2)

        # Draw X's and O's
        board_state = self.game.board.get_state()
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board_state[row, col] == 'X':
                    self._draw_x(row, col)
                elif board_state[row, col] == 'O':
                    self._draw_o(row, col)

        pygame.display.flip()  # Ensure display updates

    def display_move(self, mark, row, col):
        """Display a move using pygame."""
        rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, self.GRAY, rect)

        if mark == 'X':
            self._draw_x(row, col)
        else:
            self._draw_o(row, col)

        pygame.display.flip()
        time.sleep(0.3)  # Short pause to show the move

    def display_winner(self, mark):
        """Display the winner using pygame."""
        text = self.font.render(f"Player {mark} wins!", True, self.GREEN)
        text_rect = text.get_rect(center=(self.width // 2, self.height - 30))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

        self._wait_for_exit(3)

    def display_draw(self):
        """Display a draw using pygame."""
        text = self.font.render("Game ended in a draw!", True, self.BLUE)
        text_rect = text.get_rect(center=(self.width // 2, self.height - 30))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

        self._wait_for_exit(3)

    def _draw_x(self, row, col):
        """Draw an X on the board."""
        x = col * self.cell_size
        y = row * self.cell_size
        padding = self.cell_size // 4
        pygame.draw.line(self.screen, self.RED, (x + padding, y + padding), (x + self.cell_size - padding, y + self.cell_size - padding), 3)
        pygame.draw.line(self.screen, self.RED, (x + self.cell_size - padding, y + padding), (x + padding, y + self.cell_size - padding), 3)

    def _draw_o(self, row, col):
        """Draw an O on the board."""
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 2 - self.cell_size // 5
        pygame.draw.circle(self.screen, self.BLUE, (x, y), radius, 3)

    def _wait_for_exit(self, seconds=None):
        """Keep Pygame responsive and wait for user action or timeout."""
        start_time = time.time()

        while True:
            if seconds is not None and time.time() - start_time > seconds:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    return

            pygame.time.delay(50)  # Reduce CPU usage

    def run_main_loop(self):
        """✅ Main event loop to keep the game responsive and allow user interaction."""
        running = True
        self.display_board()  # Ensure board is drawn at start

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # ✅ Capture click and convert to row/col
                    x, y = pygame.mouse.get_pos()
                    col = x // self.cell_size
                    row = y // self.cell_size
                    self.handle_click(row, col)

            pygame.time.delay(50)  # Prevents CPU overload

    def handle_click(self, row, col):
        """Handles a player's move when they click on a cell."""
        if self.game.board.is_valid_move(row, col):
            current_player = self.game.current_player  # ✅ Get player from game instance
            self.game.board.make_move(row, col, current_player)
            self.display_board()

            # ✅ Check if game is over
            if self.game.board.is_game_over():
                winner = self.game.board.get_winner()
                if winner:
                    self.display_winner(winner)
                else:
                    self.display_draw()
                return

            # ✅ Switch player after a valid move
            self.game.switch_player()

            # ✅ If AI's turn, make the AI move automatically
            ai_agent = self.game.get_current_agent()
            if ai_agent:
                pygame.time.delay(500)  # Small delay for better experience
                ai_move = ai_agent.get_move(self.game.board)
                self.game.board.make_move(ai_move[0], ai_move[1], self.game.current_player)
                self.display_board()

                # ✅ Check if AI wins
                if self.game.board.is_game_over():
                    winner = self.game.board.get_winner()
                    if winner:
                        self.display_winner(winner)
                    else:
                        self.display_draw()
                    return

                # ✅ Switch back to human
                self.game.switch_player()
