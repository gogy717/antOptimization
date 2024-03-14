import numpy as np
import random
from numpy.random import choice as np_choice
import time


class AntColony():
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        """
        distances : 2D array
            Square matrix of distances. Diagonal is assumed to be np.inf.
        n_ants : int
            Number of ants running per iteration
        n_best : int
            Number of best ants who deposit pheromone
        n_iteration : int
            Number of iterations
        decay : float
            Rate it which pheromone decays. The pheromone value is multiplied by decay,
            so 0.95 will lead to decay, 0.5 to much faster decay.
        alpha : int or float
            Exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
        beta : int or float
            Exponent on distance, higher beta give distance more weight. Default=1
        """
        self.distances  = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        iteration_shortest_paths = []  # List to store each iteration's shortest path
        convergence_threshold = 0.01  # 定义收敛阈值
        convergence_count = 5  # 定义需要连续多少次小于阈值才认为收敛
        convergence_iterations = 0  # 初始化连续达到阈值的次数
        previous_shortest_distance = np.inf  # 初始化前一次的最短路径长度

        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            iteration_shortest_paths.append(shortest_path[1])  # Append current iteration's shortest distance
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path            
            self.pheromone = self.pheromone * self.decay
            # 判断是否收敛
            distance_improvement = previous_shortest_distance - shortest_path[1]
            if distance_improvement < convergence_threshold:
                convergence_iterations += 1
                # print(distance_improvement)
            else:
                # print(distance_improvement)
                convergence_iterations = 0  # 重置连续达到阈值的次数
            if convergence_iterations >= convergence_count:
                print(f"Algorithm has converged after {i+1} iterations.")
                break  # 收敛，跳出循环            
            previous_shortest_distance = shortest_path[1]  # 更新前一次的最短路径长度
        return all_time_shortest_path, iteration_shortest_paths, i+1  # Return the all-time shortest path and list of iteration shortest paths

    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_path_dist(self, path):
        """
        calculate the distance of the path
        """
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        """
        create a list of moves(in tuple) with length of the number of cities - 1
        """
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start)) # going back to where we started    
        return path

    def pick_move(self, pheromone, dist, visited):
        """
        轮盘赌法
        """
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)    # possibility

        norm_row = row / row.sum()
        move = np_choice(self.all_inds, 1, p=norm_row)[0]   # p is the possibility of each move
        return move



# class AntTime(AntColony):
#     def run(self):
#         start_time = time.time()  # Record the start time
#         shortest_path = None
#         all_time_shortest_path = ("placeholder", np.inf)
#         iteration_shortest_paths = []  # List to store each iteration's shortest path
#         convergence_threshold = 0.01  # 定义收敛阈值
#         convergence_count = 5  # 定义需要连续多少次小于阈值才认为收敛
#         convergence_iterations = 0  # 初始化连续达到阈值的次数
#         previous_shortest_distance = np.inf  # 初始化前一次的最短路径长度

#         for i in range(self.n_iterations):
#             all_paths = self.gen_all_paths()
#             self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)
#             shortest_path = min(all_paths, key=lambda x: x[1])
#             iteration_shortest_paths.append(shortest_path[1])  # Append current iteration's shortest distance
#             if shortest_path[1] < all_time_shortest_path[1]:
#                 all_time_shortest_path = shortest_path            
#             self.pheromone = self.pheromone * self.decay
#             # 判断是否收敛
#             distance_improvement = previous_shortest_distance - shortest_path[1]
#             if distance_improvement < convergence_threshold:
#                 convergence_iterations += 1
#                 # print(distance_improvement)
#             else:
#                 # print(distance_improvement)
#                 convergence_iterations = 0  # 重置连续达到阈值的次数
#             if convergence_iterations >= convergence_count:
#                 print(f"Algorithm has converged after {i+1} iterations.")
#                 break  # 收敛，跳出循环            
#             previous_shortest_distance = shortest_path[1]  # 更新前一次的最短路径长度
#         end_time = time.time()  # Record the end time
#         execution_time = end_time - start_time  # Calculate the execution time
#         return execution_time  # Return the all-time shortest path and list of iteration shortest paths
