import random
import time
import copy

class AlphaBetaAgent:
    def __init__(self, mark, max_depth=9):
        self.mark = mark
        self.opponent_mark = 'O' if mark == 'X' else 'X'
        self.max_depth = max_depth
        self.nodes_evaluated = 0
        self.pruned_branches = 0
        self.last_tree = None  # For visualization

    def get_move(self, board):
        self.nodes_evaluated = 0
        self.last_tree = {"root": {}}  # Always create root node

        start_time = time.time()
        valid_moves = board.get_valid_moves()

        if len(valid_moves) == 1:
            return valid_moves[0]

        best_score = float('-inf')
        best_moves = []

        root_node = self.last_tree["root"]
        root_node["children"] = {}

        for move in valid_moves:
            board_copy = copy.deepcopy(board)
            board_copy.make_move(*move, self.mark)

            node = {}
            root_node["children"][str(move)] = node

            score = self.alpha_beta(
                board_copy, self.max_depth - 1,
                alpha=float('-inf'), beta=float('inf'),
                is_maximizing=False, tree_node=node, last_move=None
            )

            node["score"] = score

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        end_time = time.time()

        from utils.metrics import MetricsCollector
        MetricsCollector().record_algorithm_stats('alphabeta', self.nodes_evaluated, end_time - start_time)

        return random.choice(best_moves)

    def alpha_beta(self, board, depth, alpha, beta, is_maximizing, tree_node=None, last_move=None):
        self.nodes_evaluated += 1

        # Create child node if visualizing
        if tree_node is not None and last_move is not None:
            move_key = f"{last_move[0]},{last_move[1]}"
            if "children" not in tree_node:
                tree_node["children"] = {}
            tree_node["children"][move_key] = {
                "state": copy.deepcopy(board.get_state()),
                "children": {},
                "score": None,
                "pruned": False
            }
            current_node = tree_node["children"][move_key]
        else:
            current_node = tree_node  # Might be the root

        # Terminal state evaluation
        winner = board.get_winner()
        if winner == self.mark:
            if current_node:
                current_node["score"] = 10 + depth
            return 10 + depth
        elif winner == self.opponent_mark:
            if current_node:
                current_node["score"] = -10 - depth
            return -10 - depth
        elif board.is_full() or depth == 0:
            if current_node:
                current_node["score"] = 0
            return 0

        valid_moves = board.get_valid_moves()

        if is_maximizing:
            max_score = float('-inf')
            for move in valid_moves:
                board_copy = copy.deepcopy(board)
                board_copy.make_move(*move, self.mark)
                score = self.alpha_beta(board_copy, depth - 1, alpha, beta, False, current_node, move)
                max_score = max(max_score, score)
                alpha = max(alpha, max_score)
                if beta <= alpha:
                    self.pruned_branches += 1
                    if current_node:
                        current_node["pruned"] = True
                    break
            if current_node:
                current_node["score"] = max_score
            return max_score
        else:
            min_score = float('inf')
            for move in valid_moves:
                board_copy = copy.deepcopy(board)
                board_copy.make_move(*move, self.opponent_mark)
                score = self.alpha_beta(board_copy, depth - 1, alpha, beta, True, current_node, move)
                min_score = min(min_score, score)
                beta = min(beta, min_score)
                if beta <= alpha:
                    self.pruned_branches += 1
                    if current_node:
                        current_node["pruned"] = True
                    break
            if current_node:
                current_node["score"] = min_score
            return min_score
