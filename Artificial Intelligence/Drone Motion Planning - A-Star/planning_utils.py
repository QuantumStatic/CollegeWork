from enum import Enum
import enum
from queue import PriorityQueue
import numpy as np
import itertools
import random
from typing import Tuple, List, Set, Union, Dict, Callable


def create_grid(data, drone_altitude, safety_distance):
    """
    Returns a grid representation of a 2D configuration space
    based on given obstacle data, drone altitude and safety distance
    arguments.
    """

    # minimum and maximum north coordinates
    north_min = np.floor(np.min(data[:, 0] - data[:, 3]))
    north_max = np.ceil(np.max(data[:, 0] + data[:, 3]))

    # minimum and maximum east coordinates
    east_min = np.floor(np.min(data[:, 1] - data[:, 4]))
    east_max = np.ceil(np.max(data[:, 1] + data[:, 4]))

    # given the minimum and maximum coordinates we can
    # calculate the size of the grid.
    north_size = int(np.ceil(north_max - north_min))
    east_size = int(np.ceil(east_max - east_min))

    # Initialize an empty grid
    grid = np.zeros((north_size, east_size))

    # Populate the grid with obstacles
    for i in range(data.shape[0]):
        north, east, alt, d_north, d_east, d_alt = data[i, :]
        if alt + d_alt + safety_distance > drone_altitude:
            obstacle = [
                int(np.clip(north - d_north - safety_distance - north_min, 0, north_size-1)),
                int(np.clip(north + d_north + safety_distance - north_min, 0, north_size-1)),
                int(np.clip(east - d_east - safety_distance - east_min, 0, east_size-1)),
                int(np.clip(east + d_east + safety_distance - east_min, 0, east_size-1)),
            ]
            grid[obstacle[0]:obstacle[1]+1, obstacle[2]:obstacle[3]+1] = 1

    return grid, int(north_min), int(east_min)


# Assume all actions cost the same.
class Action(Enum):
    """
    An action is represented by a 3 element tuple.

    The first 2 values are the delta of the action relative
    to the current grid position. The third and final value
    is the cost of performing the action.
    """

    WEST = (0, -1, 1)
    EAST = (0, 1, 1)
    NORTH = (-1, 0, 1)
    SOUTH = (1, 0, 1)

    # diagonal actions / UNCOMMMENT THIS OUT IF DIAGONAL MOVEMENTS ARE ALLOWED
    
    # NORTH_WEST = (-1, -1, pow(2, 0.5))
    # NORTH_EAST = (-1, 1, pow(2, 0.5))
    # SOUTH_WEST = (1, -1, pow(2, 0.5))
    # SOUTH_EAST = (1, 1, pow(2, 0.5))

    @property
    def cost(self):
        return self.value[2]

    @property
    def delta(self):
        return (self.value[0], self.value[1])


def valid_actions(grid, current_node):
    """
    Returns a list of valid actions given a grid and current node.
    """
    valid_actions = list(Action)
    n, m = grid.shape[0] - 1, grid.shape[1] - 1
    x, y = current_node

    # check if the node is off the grid or
    # it's an obstacle

    if x - 1 < 0 or grid[x - 1, y] == 1:
        valid_actions.remove(Action.NORTH)
    if x + 1 > n or grid[x + 1, y] == 1:
        valid_actions.remove(Action.SOUTH)
    if y - 1 < 0 or grid[x, y - 1] == 1:
        valid_actions.remove(Action.WEST)
    if y + 1 > m or grid[x, y + 1] == 1:
        valid_actions.remove(Action.EAST)

    # print(grid[0])
    # input(">")

    return valid_actions

def a_star(grid, h, start, goal):
    path = []
    path_cost = 0
    queue = PriorityQueue()
    queue.put((0, start))
    visited = set(start)

    branch = {}
    found = False
    
    while not queue.empty():
        item = queue.get()
        current_node = item[1]
        if current_node == start:
            current_cost = 0.0
        else:              
            current_cost = branch[current_node][0]
            
        if current_node == goal:        
            print('Found a path.')
            found = True
            break
        else:
            for action in valid_actions(grid, current_node):
                # get the tuple representation
                da = action.delta
                next_node = (current_node[0] + da[0], current_node[1] + da[1])
                branch_cost = current_cost + action.cost
                queue_cost = branch_cost + h(next_node, goal)
                
                if next_node not in visited:                
                    visited.add(next_node)               
                    branch[next_node] = (branch_cost, current_node, action)
                    queue.put((queue_cost, next_node))

    if found:
        # retrace steps
        n = goal
        path_cost = branch[n][0]
        path.append(goal)
        while branch[n][1] != start:
            path.append(branch[n][1])
            n = branch[n][1]
        path.append(branch[n][1])
    else:
        print('**********************')
        print('Failed to find a path!')
        print('**********************') 
    return path[::-1], path_cost

def heuristic(position, goal_position):
    return np.linalg.norm(np.array(position) - np.array(goal_position))

def iterative_a_star(grid:np.ndarray, h:Callable, start:Tuple[int, int], goal:Tuple[int, int], verbose:bool=True) -> Tuple[List[Tuple[int, int]], float]:
    """
    Iterative version of the A* algorithm.

    :param grid: A 2D array of 0's and 1's.

    :param h: Heuristic function used to estimate distances between two points.
    :type h: function [heuristic(position, goal_position) -> float]

    :param start: Start position as a tuple in (north, east) order

    :param goal: Goal position as a tuple in (north, east) order

    :return: Returns a tuple containg a list of lowest cost path and the lowest cost path.
    """


    # initial threshold is the heuristic cost from start to goal
    f_limit:float = h(start, goal)

    while True:
        branches, new_path_cost = search_with_f_limit(grid, h, start, goal, f_limit)
        
        # if the new path cost is equal to the threshold, then no node was found that was greater than the threshold and the path is complete
        if new_path_cost == f_limit:
            if verbose:
                print("*"*20)
                print("Found a path with a cost of {:.3f}".format(branches[goal][1]))
                print("*"*20)
            path = []
            n = goal
            path.append(goal)
            while branches[n][0] != start:
                path.append(branches[n][0])
                n = branches[n][0]
            path.append(branches[n][0])

            # remove redundant points
            if verbose:
                print("Removing some redundant points...")
            path = remove_redundant_points(path, {start, goal})

            return path, branches[goal][1]
        
        # update the threshold to the new path cost of the closest node that did not fit the current threshold
        # a small margin is added to the new threshold to avoid the case where the new threshold is similar to the previous one
        f_limit = new_path_cost ** 1.15

def search_with_f_limit(grid:np.ndarray, h:Callable, start:Tuple[int, int], goal:Tuple[int, int], f_limit:float) -> Tuple[Union[Dict[Tuple[int, int], Tuple[int, int]], None], float]:
    """
    Performs a search with a given threshold referred as f_limit.

    :param grid: A 2D array of 0's and 1's.

    :param h: Heuristic function used to estimate distances between two points.

    :param start: Start position as a tuple in (north, east) order

    :param goal: Goal position as a tuple in (north, east) order

    :param f_limit: The threshold for the search.

    :return: Returns a tuple containg a dictionary of branches and the lowest cost path.

    """
    visited = {start}
    node_distances = {start: 0}
    p_queue = PriorityQueue()
    p_queue.put((0, start))

    new_min_f_limit = float('inf')
    branches = {}

    while not p_queue.empty():
        item = p_queue.get()
        current_node = item[1]

        if current_node == goal:
            # Add the cost to the branches
            branches[goal] = (branches[goal][0], node_distances[goal])
            return branches, f_limit

        for action in valid_actions(grid, current_node):
            da = action.delta
            next_node = (current_node[0] + da[0], current_node[1] + da[1])

            if next_node not in visited:
                next_node_costs = h(next_node, goal) + node_distances[current_node] + action.cost 
                node_distances[next_node] = node_distances[current_node] + action.cost
                if next_node_costs <= f_limit:
                    visited.add(next_node)
                    branches[next_node] = tuple([current_node])
                    p_queue.put((next_node_costs, next_node))
                elif next_node_costs < new_min_f_limit:
                    new_min_f_limit = next_node_costs

    return None, new_min_f_limit


# Heuristics for Question 3


def manhattan_heuristic(position:Tuple[int, int], goal_position:Tuple[int, int]) -> int:
    """
    Calculates and returns the manhattan distance between two points

    :param position: First point.

    :param goal_position: Second point.

    :return: Returns the manhattan distance between two points.
    """
    return abs(position[0] - goal_position[0]) + abs(position[1] - goal_position[1])

def chebyshev_heuristic(position:Tuple[int, int], goal_position:Tuple[int, int]) -> int:
    """
    Calculates and returns the chebyshev distance between two points

    :param position: First point.

    :param goal_position: Second point.

    :return: Returns the chebyshev distance between two points.
    """
    return max(abs(position[0] - goal_position[0]), abs(position[1] - goal_position[1]))

def minkowski_heuristic(position:Tuple[int, int], goal_position:Tuple[int, int]) -> float:
    """
    Calculates the minkowski distance between two points and uses it as a distance metric

    :param position: First point.

    :param goal_position: Second point.

    :return: Returns the minkowski distance between two points.
    """
    p = 4
    return ((abs(position[0] - goal_position[0]))**p + (abs(position[1] - goal_position[1]))**p)**(1/p)

def canny_heuristic(position:Tuple[int, int], goal_position:Tuple[int, int]) -> float:
    """
    A function that calculates canny similarity between two points and uses it as a distance metric

    :param position: First point.

    :param goal_position: Second point.

    :return: Returns the canny similarity between two points.
    """
    h_val = 0
    for x in range(2):
        h_val += (np.abs(goal_position[x] - position[x]) / (abs(goal_position[x]) + abs(position[x])))

    return h_val

def cosine_heuristic(position:Tuple[int, int], goal_position:Tuple[int, int]) -> float:
    """
    A function that calculates cosine similarity between two points and uses it as a distance metric

    :param position: First point.

    :param goal_position: Second point.

    :return: Returns the cosine similarity between two points.
    """
    return np.dot(position, goal_position) / ((np.linalg.norm(position) * np.linalg.norm(goal_position)))

def braycurtis_heuristic(position:Tuple[int, int], goal_position:Tuple[int, int]) -> float:
    """
    Returns the braycurtis distance between two points.

    :param position: First point.

    :param goal_position: Second point.

    :return: Returns the braycurtis distance between two points.
    """
    return (abs(goal_position[0] - position[0]) + abs(goal_position[1] - position[1])) / (abs(goal_position[0] + position[0]) + abs(goal_position[1] + position[1]))

def hamm_heuristic(position:Tuple[int, int], goal_position:Tuple[int, int]) -> int:
    """
    Returns the hamming distance between two points.

    :param position: First point.

    :param goal_position: Second point.

    :return: Returns the hamming distance between two points.
    """
    new_position = [0]*2
    new_goal_position = [0]*2
    for x in range(2):
        new_position[x] = bin(position[x])[2:].rjust(11, '0')
        new_goal_position[x] = bin(goal_position[x])[2:].rjust(11, '0')
    new_position = "".join(new_position)
    new_goal_position = "".join(new_goal_position)
    return sum(ch1 != ch2 for ch1, ch2 in zip(new_position, new_goal_position))


# N point a star for Question 4

def get_closest_point(points:Tuple[Tuple[int, int], ...], point:Tuple[int, int], h:Callable) -> Tuple[Tuple[int, int], float]:
    """
    Returns the closest point to the given point.

    :param points: List of points to search.

    :param point: Point to search for.

    :param h: Heuristic function to use.
    """
    min_dist, min_point = float('inf'), None
    for p in points:
        dist = h(p, point)
        if dist < min_dist:
            min_dist, min_point = dist, p
    return min_point, min_dist

def get_min_cost_path(h:Callable, start:Tuple[int, int], goal:Tuple[int, int], points:Tuple[Tuple[int, int], ...] , n_pts:int) -> Tuple[List[Tuple[int, int]], float]:
    """
    Returns the minimum cost path for the given points and the cost of the path. 

    :param h: Heuristic function to use.

    :param start: Start point.

    :param goal: Goal point.

    :param points: List of points to visit.

    :param n_pts: Number of points to visit.
    """
    min_cost_permutation, min_cost = None, float('inf')
    
    if n_pts < 7:
        # Brute Force for small number of points.
        for permutation in itertools.permutations(range(len(points))):
            estimated_cost = 0
            for x, idx in enumerate(permutation):
                if x == 0:
                    estimated_cost += h(start, points[idx])
                elif x == len(points) - 1:
                    estimated_cost += h(points[idx], goal)
                else:
                    estimated_cost += h(points[idx], points[permutation[x + 1]])

            if estimated_cost < min_cost:
                min_cost_permutation, min_cost = permutation, estimated_cost
        
        fin_path = [start]
        
        for idx in min_cost_permutation:
            fin_path.append(points[idx])
        
        return fin_path + [goal], min_cost
    else:
        # Greedy for large number of points.
        pts_cpy = set(points)
        greedy_min_cost_permutation, greedy_min_cost = [start], float('inf')
        while len(pts_cpy) > 0:
            min_point, min_dist = get_closest_point(pts_cpy, greedy_min_cost_permutation[-1], h)
            greedy_min_cost += min_dist
            greedy_min_cost_permutation.append(min_point)
            pts_cpy.remove(min_point)
        
        return greedy_min_cost_permutation + [goal], greedy_min_cost

def iter_a_star_n_points(grid:np.ndarray, h:Callable, start:Tuple[int, int], goal:Tuple[int, int], fixed_pts:Tuple[Tuple[int, int], ...] = None, generate_points: int = 3, verbose:bool=True) -> Tuple[List[Tuple[int, int]], float]:
    """
    A* algorithm for a grid with must pass points.

    :param grid: 2D numpy array representing the grid

    :param h: Heuristic function to use

    :param start: Start position

    :param goal: Goal position
    
    :param fixed_pts: Fixed points to pass through

    :param generate_points: Number of random points to generate

    :param verbose: Print the path and cost

    :return: Path and cost
    """

    # generating random points fixed points according to the last question, default value is 3 according to the question
    if fixed_pts is not None:
        points = fixed_pts
        total_points = len(fixed_pts)
    else:
        points = generate_random_points(grid, start, goal, generate_points)
        total_points = generate_points

    # tried to use the greedy algorithm to find the most optimum path or if total points are less than 7, then use brute force
    min_cost_permutation, min_cost = get_min_cost_path(h, start, goal, points, total_points)

    # Display the path and cost
    if verbose:
        print("optimum path found with cost {}".format(min_cost))
        print("Most optimum route according to heuristic is:")
        route_str = ""
        for point in min_cost_permutation[:-1]:
            route_str += "{} -> ".format(point)
        route_str += "{}".format(goal)
        print(route_str)
        print("starting path finding")
    
    final_path = []

    # using iterative a star to find the path
    total_cost = 0
    for x in range(total_points + 1):
        path, curr_cost = iterative_a_star(grid, h, min_cost_permutation[x + 1], min_cost_permutation[x])
        final_path = final_path + path[1:] if any(final_path) else path
        if verbose:
            print("{}/{} complete".format(x + 1, total_points + 1))
        total_cost += curr_cost

    return final_path, total_cost


# general helper functions

# Collinearity Check to remove some waypoints
def collinearity_check(p1:Tuple[int, int], p2: Tuple[int, int], epsilon:float=1e-2) -> bool:
    """
    Checks if the points p1 and p2 are collinear however, this is a primitive method and is not robust

    :param p1: (x, y) coordinate of the first point

    :param p2: (x, y) coordinate of the second point

    :param epsilon: threshold for collinearity

    :return: True if the points are collinear, False otherwise
    """
    return (abs(p1[0] - p2[0]) <= epsilon) or (abs(p1[1] - p2[1]) <= epsilon)

def remove_redundant_points(path:List[Tuple[int, int]], non_removable_points:Set[Tuple[int,int]]=None) -> List[Tuple[int, int]]:
    """
    Removes redundant points from a path performing a collinearity check

    :param path: List of (x, y) coordinates of the path

    :param non_removable_points: Set of (x, y) coordinates of points that should not be removed

    :return: List of (x, y) coordinates of the path with redundant points removed
    """
    path_cpy = path.copy()

    if non_removable_points is None:
        non_removable_points = set()

    prev_waypoint = path[0]
    for point in path[1:]:
        # Remove collinear points
        if collinearity_check(prev_waypoint, point) and point not in non_removable_points:
            path_cpy.remove(point)
        else:
            prev_waypoint = point
    return path_cpy

def generate_random_points(grid:np.ndarray, start:Tuple[int, int], goal:Tuple[int, int], pts:int=2) -> Tuple[Tuple[int, int], ...]:
    """
    A function that generates points within a 40 unit radius of start and goal.

    :param grid: 2D numpy array representing the grid

    :param start: Tuple of (x, y) coordinates of the start point

    :param goal: Tuple of (x, y) coordinates of the goal point

    :param pts: Number of points to generate, defaults to 2

    :return: Tuple of (x, y) coordinates of the generated points
    """

    found_register, points = {start, goal}, []
    radius = 20

    n, m = grid.shape[0] - 1, grid.shape[1] - 1

    while len(points) < pts:
        # Points based on start and goal
        point_to_use = start if random.choice((True, False)) else goal

        # Random point within 40 units of start or goal
        proposed_point = (random.randint(point_to_use[0], point_to_use[0] + 40) - radius, random.randint(point_to_use[1], point_to_use[1] + 40) - radius)
        
        if proposed_point in points:
            continue

        # Check if point is within grid
        if proposed_point[0] < 0 or proposed_point[0] > n or proposed_point[1] < 0 or proposed_point[1] > m:
            found_register.add(proposed_point)
            continue
        
        points.append(proposed_point)
        found_register.add(proposed_point)

    return tuple(points)