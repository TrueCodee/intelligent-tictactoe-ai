import os
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Patch
import time

class TreeVisualizer:
    def __init__(self):
        """Initialize the tree visualizer."""
        os.makedirs("results/visualizations", exist_ok=True)

    def visualize(self, tree_data, filename_prefix):
        """
        Visualize a decision tree.

        Args:
            tree_data (dict): Tree data structure.
            filename_prefix (str): Prefix for the output filename.
        """
        if tree_data is None:
            print("No tree data available for visualization.")
            return

        # Create a directed graph
        G = nx.DiGraph()
        node_labels = {}
        node_colors = []

        # Build the graph recursively
        self._build_graph(G, tree_data, "root", None, node_labels, node_colors)

        # Use a custom top-down layout
        pos = self._hierarchical_layout(G)

        # Draw the graph
        plt.figure(figsize=(15, 10))
        print(f"[TreeVisualizer] Nodes: {len(G.nodes)}, Colors: {len(node_colors)}")

        colors_to_use = node_colors[:len(G.nodes)]

        nx.draw(
            G, pos, with_labels=True, labels=node_labels,
            node_color=colors_to_use,
            node_size=1500, font_size=8, edge_color="gray"
        )

        # Add color legend
        legend_elements = [
            Patch(facecolor='lightgreen', edgecolor='gray', label='Winning move'),
            Patch(facecolor='lightblue', edgecolor='gray', label='Losing move'),
            Patch(facecolor='lightyellow', edgecolor='gray', label='Neutral / Draw'),
            Patch(facecolor='red', edgecolor='gray', label='Pruned (Alpha-Beta)'),
            Patch(facecolor='white', edgecolor='gray', label='Unknown / Unscored'),
        ]
        plt.legend(handles=legend_elements, loc='lower left')

        # Save the visualization
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"results/visualizations/{filename_prefix}_tree_{timestamp}.png"
        plt.savefig(filename)
        plt.close()
        print(f"✅ Decision tree visualization saved as: {filename}")

    def _build_graph(self, G, node_data, node_id, parent_id, node_labels, node_colors):
        """
        Recursively builds the graph for visualization.

        Args:
            G (nx.DiGraph): Graph object.
            node_data (dict): Tree node data.
            node_id (str): Current node ID.
            parent_id (str): Parent node ID.
            node_labels (dict): Dictionary for node labels.
            node_colors (list): List for node colors.
        """
        G.add_node(node_id)
        node_labels[node_id] = node_id if node_id == "root" else f"{node_data.get('score', 'N/A')}"

        # Determine node color based on score
        if node_data.get("pruned"):
            node_colors.append("red")
        elif "score" in node_data:
            score = node_data["score"]
            if score > 0:
                node_colors.append("lightgreen")
            elif score < 0:
                node_colors.append("lightblue")
            else:
                node_colors.append("lightyellow")
        else:
            node_colors.append("white")

        # Connect to parent
        if parent_id:
            G.add_edge(parent_id, node_id)

        # Recurse for children
        for move, child_data in node_data.get("children", {}).items():
            self._build_graph(G, child_data, move, node_id, node_labels, node_colors)

    def _hierarchical_layout(self, G, root="root", width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, visited=None):
        """
        A safe recursive top-down layout for trees (no Graphviz).
        """
        if pos is None:
            pos = {}
        if visited is None:
            visited = set()
        visited.add(root)

        children = [n for n in G.neighbors(root) if n not in visited]

        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = self._hierarchical_layout(G, root=child, width=dx, vert_gap=vert_gap,
                                                vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                                parent=root, visited=visited)
        pos[root] = (xcenter, vert_loc)
        return pos

