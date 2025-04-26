import time
import pygame
import sys
from game.game import TicTacToe
from agents.human_agent import HumanAgent
from agents.minimax_agent import MinimaxAgent
from agents.alphabeta_agent import AlphaBetaAgent
from agents.gemini_agent import GeminiAgent
from utils.logger import Logger
from utils.metrics import MetricsCollector
from visualization.console_view import ConsoleView
from visualization.gui_view import GUIView
from visualization.tree_visualizer import TreeVisualizer

def get_agent(agent_type, mark, depth=9):
    """Returns the appropriate agent based on the selected type."""
    if agent_type == 'human':
        return HumanAgent(mark)
    elif agent_type == 'minimax':
        return MinimaxAgent(mark, depth)
    elif agent_type == 'alphabeta':
        return AlphaBetaAgent(mark, depth)
    elif agent_type == 'gemini':
        return GeminiAgent(mark)
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")

# (imports remain unchanged)

def main():
    print("\n🎮 Welcome to Tic-Tac-Toe with AI! 🎮")

    # Game Mode Selection
    print("\nSelect Game Mode:")
    print("1️⃣  Human vs Minimax")
    print("2️⃣  Human vs Alpha-Beta")
    print("3️⃣  Human vs Gemini")
    print("4️⃣  Minimax vs Alpha-Beta")
    print("5️⃣  AI vs AI (Custom)")
    print("6️⃣  Benchmark Mode")
    mode = int(input("\nEnter mode (1-6): "))

    # Visualization Mode
    print("\nSelect Visualization Mode:")
    print("1️⃣  Console Mode")
    print("2️⃣  GUI (Pygame)")
    viz_choice = int(input("\nEnter visualization mode (1 for Console, 2 for GUI): "))
    viz = 'console' if viz_choice == 1 else 'gui'

    # Board Size
    size = int(input("\nEnter board size (3 for 3x3, 5 for 5x5): "))

    # Depth Selection
    depth = 9
    if mode in [1, 2, 4, 5]:
        depth = int(input("\nEnter AI search depth (default: 9): "))

    # Logger and Metrics
    logger = Logger("game_log.txt")
    metrics = MetricsCollector()

    # Visualization Setup
    if viz == 'console':
        view = ConsoleView()
    else:
        print("Launching Pygame GUI...")
        pygame.init()
        game_stub = TicTacToe(board_size=size)
        view = GUIView(game_stub)

    tree_viz = TreeVisualizer() if mode in [1, 2, 4, 5] else None

    # Agent Configuration
    if mode == 1:
        agent1 = HumanAgent('X')
        agent2 = MinimaxAgent('O', depth)
    elif mode == 2:
        agent1 = HumanAgent('X')
        agent2 = AlphaBetaAgent('O', depth)
    elif mode == 3:
        agent1 = HumanAgent('X')
        agent2 = GeminiAgent('O')
    elif mode == 4:
        agent1 = MinimaxAgent('X', depth)
        agent2 = AlphaBetaAgent('O', depth)
    elif mode == 5:
        valid_choices = ['minimax', 'alphabeta', 'gemini']
        player1 = input("\nSelect AI for Player 1 (X) [minimax / alphabeta / gemini]: ").strip().lower()
        while player1 not in valid_choices:
            print("❌ Invalid choice!")
            player1 = input("Select AI for Player 1 (X): ").strip().lower()
        player2 = input("\nSelect AI for Player 2 (O) [minimax / alphabeta / gemini]: ").strip().lower()
        while player2 not in valid_choices:
            print("❌ Invalid choice!")
            player2 = input("Select AI for Player 2 (O): ").strip().lower()
        agent1 = get_agent(player1, 'X', depth)
        agent2 = get_agent(player2, 'O', depth)
    elif mode == 6:
        run_benchmark(size, depth, logger, metrics)
        return

    game = TicTacToe(board_size=size, agent1=agent1, agent2=agent2,
                     view=view, metrics=metrics, tree_viz=tree_viz)

    if viz == 'gui':
        view.game = game
        view.run_main_loop()
    else:
        winner = game.play()

        if winner is None:
            logger.log("Game ended in a draw")
        else:
            logger.log(f"Winner: {winner}")

        metrics.save_to_file(f"results/metrics/game_{time.strftime('%Y%m%d_%H%M%S')}.json")

        print("\n📊 Game Statistics:")
        print(f"Total nodes evaluated by Minimax: {metrics.get_nodes_evaluated('minimax')}")
        print(f"Total nodes evaluated by Alpha-Beta: {metrics.get_nodes_evaluated('alphabeta')}")
        print(f"Execution time for Minimax: {metrics.get_execution_time('minimax'):.4f} seconds")
        print(f"Execution time for Alpha-Beta: {metrics.get_execution_time('alphabeta'):.4f} seconds")

        # Visualize Tree if applicable
        if tree_viz:
            if isinstance(agent2, AlphaBetaAgent) and agent2.last_tree:
                tree_viz.visualize(agent2.last_tree["root"], "alphabeta_tree")
            elif isinstance(agent2, MinimaxAgent) and agent2.last_tree:
                tree_viz.visualize(agent2.last_tree["root"], "minimax_tree")

    if viz == "gui":
        print("Game over. Close the Pygame window to exit.")
        pygame.quit()
        sys.exit()

def run_benchmark(size, depth, logger, metrics):
    print(f"\n🏆 Running benchmark on {size}x{size} board...")

    if size == 5 and depth > 4:
        print("⚠️ Reducing depth to 3 for 5x5 benchmark to prevent timeout.")
        depth = 3

    view = ConsoleView()  # Use text mode for benchmarking

    ai_combos = [
        ('minimax', 'minimax'),
        ('alphabeta', 'alphabeta'),
        ('minimax', 'alphabeta'),
        ('minimax', 'gemini'),
        ('alphabeta', 'gemini')
    ]

    for ai1, ai2 in ai_combos:
        print(f"\n🚀 Testing {ai1} (X) vs {ai2} (O)...")
        wins = {'X': 0, 'O': 0, 'draw': 0}

        for i in range(5):  # Reduce to 5 games for speed
            metrics.reset()
            agent1 = get_agent(ai1, 'X', depth)
            agent2 = get_agent(ai2, 'O', depth)
            game = TicTacToe(board_size=size, agent1=agent1, agent2=agent2,
                             view=view, metrics=metrics, tree_viz=None, quiet=True)
            winner = game.play()
            if winner:
                wins[winner] += 1
            else:
                wins['draw'] += 1

            metrics.save_to_file(f"results/metrics/benchmark_{ai1}_vs_{ai2}_game{i+1}.json")

        print(f"{ai1} (X) vs {ai2} (O): {wins['X']} Wins | {wins['O']} Wins | {wins['draw']} Draws")

    print("\n📊 Benchmark complete.")

if __name__ == "__main__":
    main()
