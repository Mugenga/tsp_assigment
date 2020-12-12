# Solving The Traveling Salesman Problem using Branch and Bound.
import math

maxsize = float('inf')


# Method to copy temporary solution to the final solution
def copy_to_final(curr_path):
    final_solution[:N + 1] = curr_path[:]
    final_solution[N] = curr_path[0]


# method to find the minimum edge cost having an end at the vertex value
def first_min(adj, value):
    min_ = maxsize
    for k in range(N):
        if adj[value][k] < min_ and value != k:
            min_ = adj[value][k]

    return min_


# Method to find the second minimum edge cost having an end at the vertex value
def second_min(adj, value):
    first, second = maxsize, maxsize
    for j in range(N):
        if value == j:
            continue
        if adj[value][j] <= first:
            second = first
            first = adj[value][j]

        elif (adj[value][j] <= second and
              adj[value][j] != first):
            second = adj[value][j]

    return second


# Method that takes as arguments:
# curr_bound -> lower bound of the root node
# curr_weight-> stores the weight of the path so far
# level-> current level while moving
# in the search space tree
# curr_path[] -> where the solution is being stored
# which would later be copied to final_path[]
def tsp_recursion(adj, curr_bound, curr_weight,
                  level, curr_path, was_visited):
    global final_min_res

    # Check if we have covered all the nodes once
    if level == N:
        # Check if there is an edge from last vertex
        if adj[curr_path[level - 1]][curr_path[0]] != 0:

            # curr_res has the total weight
            curr_res = curr_weight + adj[curr_path[level - 1]] \
                [curr_path[0]]
            if curr_res < final_min_res:
                copy_to_final(curr_path)
                final_min_res = curr_res
        return

    # Iterate for all vertices to build the search space tree recursively for any other level
    for value in range(N):

        # Consider next vertex if it is not same
        if (adj[curr_path[level - 1]][value] != 0 and
                was_visited[value] == False):
            temp = curr_bound
            curr_weight += adj[curr_path[level - 1]][value]

            # different computation of curr_bound
            # for level 2 from the other levels
            if level == 1:
                curr_bound -= ((first_min(adj, curr_path[level - 1]) +
                                first_min(adj, value)) / 2)
            else:
                curr_bound -= ((second_min(adj, curr_path[level - 1]) +
                                first_min(adj, value)) / 2)

            # curr_bound + curr_weight is the actual lower bound
            # for the node that we have arrived on.
            # If current lower bound < final_res,
            # we need to explore the node further
            if curr_bound + curr_weight < final_min_res:
                curr_path[level] = value
                was_visited[value] = True

                # call TSPRec for the next level
                tsp_recursion(adj, curr_bound, curr_weight,
                              level + 1, curr_path, was_visited)

            # Else we have to prune the node by resetting
            # all changes to curr_weight and curr_bound
            curr_weight -= adj[curr_path[level - 1]][value]
            curr_bound = temp

            # Also reset the visited array
            was_visited = [False] * len(was_visited)
            for j in range(level):
                if curr_path[j] != -1:
                    was_visited[curr_path[j]] = True


# This function sets up final_path
def tsp(adj):
    # Calculate initial lower bound for the root node
    # using the formula 1/2 * (sum of first min +
    # second min) for all edges. Also initialize the
    # curr_path and visited array
    curr_bound = 0
    curr_path = [-1] * (N + 1)
    visited = [False] * N

    # Compute initial bound
    for i in range(N):
        curr_bound += (first_min(adj, i) +
                       second_min(adj, i))

    # Rounding off the lower bound to an integer
    curr_bound = math.ceil(curr_bound / 2)

    # We start at vertex 1 so the first vertex
    # in curr_path[] is 0
    visited[0] = True
    curr_path[0] = 0

    # Call to TSPRec for curr_weight
    # equal to 0 and level 1
    tsp_recursion(adj, curr_bound, 0, 1, curr_path, visited)

######################################################

# CODE START HERE

# Adjacency matrix for the graph in Part 2 Question 1


matrix = [[0, 10, 8, 9, 7],
          [10, 0, 10, 5, 6],
          [8, 10, 0, 8, 9],
          [9, 5, 8, 0, 6],
          [7, 6, 9, 6, 0]]

# No of Edges
N = 5

# Stores the final solution
final_solution = [None] * (N + 1)

# visited[] keeps track of the already
# visited nodes in a particular path
track_visited = [False] * N

# Stores the final minimum weight of shortest tour.
final_min_res = maxsize

tsp(matrix)

print("Minimum cost :", final_min_res)
print("Path Taken : ", end=' ')
for i in range(N + 1):
    print(final_solution[i], end=' ')
