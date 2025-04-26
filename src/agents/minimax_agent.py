import random
import time
import copy

class MinimaxAgent:
    def __init__(self, mark, max_depth=9):
        self.mark = mark
        self.opponent_mark = 'O' if mark == 'X' else 'X'
        self.max_depth = max_depth
        self.nodes_evaluated = 0
        self.last_tree = None

    def get_move(self, board):
        self.nodes_evaluated = 0
        start_time = time.time()

        valid_moves = board.get_valid_moves()

        if len(valid_moves) == 1:
            return valid_moves[0]

        # Prepare tree visualization structure
        self.last_tree = {"root": {"state": copy.deepcopy(board.get_state()), "children": {}}}
        root_node = self.last_tree["root"]

        best_score = float('-inf')
        best_moves = []

        for move in valid_moves:
            board_copy = copy.deepcopy(board)
            board_copy.make_move(*move, self.mark)

            node = {}
            root_node["children"][str(move)] = node

            score = self.minimax(
                board_copy, self.max_depth - 1, False,
                float('-inf'), float('inf'), node
            )
            node["score"] = score

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        end_time = time.time()

        from utils.metrics import MetricsCollector
        MetricsCollector().record_algorithm_stats('minimax', self.nodes_evaluated, end_time - start_time)

        return random.choice(best_moves)

    def minimax(self, board, depth, is_maximizing, alpha, beta, tree_node=None):
        self.nodes_evaluated += 1

        winner = board.get_winner()
        if winner == self.mark:
            if tree_node is not None:
                tree_node["score"] = 10 + depth
            return 10 + depth
        elif winner == self.opponent_mark:
            if tree_node is not None:
                tree_node["score"] = -10 - depth
            return -10 - depth
        elif board.is_full() or depth == 0:
            if tree_node is not None:
                tree_node["score"] = 0
            return 0

        valid_moves = board.get_valid_moves()
        if tree_node is not None:
            tree_node["children"] = {}

        if is_maximizing:
            max_score = float('-inf')
            for move in valid_moves:
                board_copy = copy.deepcopy(board)
                board_copy.make_move(*move, self.mark)

                child_node = {}
                if tree_node is not None:
                    tree_node["children"][str(move)] = child_node

                score = self.minimax(board_copy, depth - 1, False, alpha, beta, child_node)
                max_score = max(max_score, score)
                alpha = max(alpha, score)
            if tree_node is not None:
                tree_node["score"] = max_score
            return max_score

        else:
            min_score = float('inf')
            for move in valid_moves:
                board_copy = copy.deepcopy(board)
                board_copy.make_move(*move, self.opponent_mark)

                child_node = {}
                if tree_node is not None:
                    tree_node["children"][str(move)] = child_node

                score = self.minimax(board_copy, depth - 1, True, alpha, beta, child_node)
                min_score = min(min_score, score)
                beta = min(beta, score)
            if tree_node is not None:
                tree_node["score"] = min_score
            return min_score
