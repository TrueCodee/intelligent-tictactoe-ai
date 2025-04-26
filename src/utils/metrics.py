import os
import json
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class MetricsCollector:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MetricsCollector, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self.reset()
            
            # Create directories
            os.makedirs("results/metrics", exist_ok=True)
            os.makedirs("results/visualizations", exist_ok=True)
    
    def reset(self):
        """Reset all metrics."""
        self.algorithm_stats = {
            'minimax': {'nodes_evaluated': 0, 'execution_time': 0, 'move_times': []},
            'alphabeta': {'nodes_evaluated': 0, 'execution_time': 0, 'move_times': [], 'pruned_branches': 0},
            'gemini': {'nodes_evaluated': 0, 'execution_time': 0, 'move_times': []},
        }
        self.benchmark_results = {}
    
    def record_algorithm_stats(self, algorithm, nodes_evaluated, execution_time):
        """
        Record algorithm statistics.
        
        Args:
            algorithm (str): The algorithm name ('minimax', 'alphabeta', or 'gemini')
            nodes_evaluated (int): Number of nodes evaluated
            execution_time (float): Execution time in seconds
        """
        if algorithm in self.algorithm_stats:
            self.algorithm_stats[algorithm]['nodes_evaluated'] += nodes_evaluated
            self.algorithm_stats[algorithm]['execution_time'] += execution_time
    
    def record_move_time(self, algorithm, time_taken):
        """
        Record time taken for a move.
        
        Args:
            algorithm (str): The algorithm name
            time_taken (float): Time taken for the move in seconds
        """
        if algorithm in self.algorithm_stats:
            self.algorithm_stats[algorithm]['move_times'].append(time_taken)
    
    def record_pruned_branches(self, algorithm, pruned_branches):
        """
        Record number of pruned branches.
        
        Args:
            algorithm (str): The algorithm name
            pruned_branches (int): Number of pruned branches
        """
        if algorithm in self.algorithm_stats and 'pruned_branches' in self.algorithm_stats[algorithm]:
            self.algorithm_stats[algorithm]['pruned_branches'] += pruned_branches
    
    def get_nodes_evaluated(self, algorithm):
        """
        Get the number of nodes evaluated by an algorithm.
        
        Args:
            algorithm (str): The algorithm name
            
        Returns:
            int: Number of nodes evaluated
        """
        if algorithm in self.algorithm_stats:
            return self.algorithm_stats[algorithm]['nodes_evaluated']
        return 0
    
    def get_execution_time(self, algorithm):
        """
        Get the execution time of an algorithm.
        
        Args:
            algorithm (str): The algorithm name
            
        Returns:
            float: Execution time in seconds
        """
        if algorithm in self.algorithm_stats:
            return self.algorithm_stats[algorithm]['execution_time']
        return 0
    
    def get_pruned_branches(self, algorithm):
        """
        Get the number of pruned branches.
        
        Args:
            algorithm (str): The algorithm name
            
        Returns:
            int: Number of pruned branches
        """
        if algorithm in self.algorithm_stats and 'pruned_branches' in self.algorithm_stats[algorithm]:
            return self.algorithm_stats[algorithm]['pruned_branches']
        return 0
    
    def save_to_file(self, filename):
        """
        Save metrics to a file.
        
        Args:
            filename (str): The filename
        """
        with open(filename, 'w') as f:
            json.dump(self.algorithm_stats, f, indent=4)
    
    def save_benchmark_results(self, filename):
        """
        Save benchmark results to a file.
        
        Args:
            filename (str): The filename
        """
        self.benchmark_results = self.algorithm_stats
        with open(filename, 'w') as f:
            json.dump(self.benchmark_results, f, indent=4)
    
    def generate_comparative_charts(self):
        """Generate comparative charts for visualization."""
        # Create directories if they don't exist
        os.makedirs("results/visualizations", exist_ok=True)
        
        # Only generate charts if we have data
        if not self.algorithm_stats['minimax']['move_times'] and not self.algorithm_stats['alphabeta']['move_times']:
            return
        
        # Prepare data
        algorithms = []
        nodes_evaluated = []
        execution_times = []
        avg_move_times = []
        
        for alg, stats in self.algorithm_stats.items():
            if stats['nodes_evaluated'] > 0:
                algorithms.append(alg)
                nodes_evaluated.append(stats['nodes_evaluated'])
                execution_times.append(stats['execution_time'])
                avg_move_times.append(sum(stats['move_times']) / len(stats['move_times']) if stats['move_times'] else 0)
        
        # Chart 1: Nodes Evaluated
        plt.figure(figsize=(10, 6))
        plt.bar(algorithms, nodes_evaluated)
        plt.title('Nodes Evaluated Comparison')
        plt.xlabel('Algorithm')
        plt.ylabel('Number of Nodes')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig('results/visualizations/nodes_evaluated_comparison.png')
        plt.close()
        
        # Chart 2: Execution Time
        plt.figure(figsize=(10, 6))
        plt.bar(algorithms, execution_times)
        plt.title('Execution Time Comparison')
        plt.xlabel('Algorithm')
        plt.ylabel('Time (seconds)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig('results/visualizations/execution_time_comparison.png')
        plt.close()
        
        # Chart 3: Average Move Time
        plt.figure(figsize=(10, 6))
        plt.bar(algorithms, avg_move_times)
        plt.title('Average Move Time Comparison')
        plt.xlabel('Algorithm')
        plt.ylabel('Time (seconds)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig('results/visualizations/avg_move_time_comparison.png')
        plt.close()
        
        # If we have pruning data, create a chart for that too
        if 'pruned_branches' in self.algorithm_stats['alphabeta']:
            pruned = self.algorithm_stats['alphabeta']['pruned_branches']
            evaluated = self.algorithm_stats['alphabeta']['nodes_evaluated']
            
            # Only create chart if we have meaningful data
            if evaluated > 0:
                labels = ['Evaluated Nodes', 'Pruned Branches']
                sizes = [evaluated, pruned]
                
                plt.figure(figsize=(8, 8))
                plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                plt.axis('equal')
                plt.title('Alpha-Beta Pruning Efficiency')
                plt.savefig('results/visualizations/alphabeta_pruning_efficiency.png')
                plt.close()