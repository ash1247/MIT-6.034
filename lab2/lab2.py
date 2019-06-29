# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    visited, agenda = set(), [(start, [start])]
    while agenda:
        (node, path) = agenda.pop(0)
        visited.add(node)
        if node == goal:
            return path
        nodes = graph.get_connected_nodes(node)
        for n in nodes: 
            if not n in visited:
                agenda.append((n, path + [n]))

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    visited, agenda = set(), [(start, [start])]
    while agenda:
        (node, path) = agenda.pop()
        visited.add(node)
        if node == goal:
            return path
        nodes = graph.get_connected_nodes(node)
        for n in nodes: 
            if not n in visited:
                agenda.append((n, path + [n]))


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    visited, agenda = set(), [(start, [start])]
    while agenda:
        (node, path) = agenda.pop()
        visited.add(node)
        if node == goal:
            return path
        nodes = sorted(graph.get_connected_nodes(node), 
                key = (lambda x: graph.get_heuristic(x, goal)), reverse=True)
        for n in nodes:
            if not n in visited:
                agenda.append((n, path + [n]))

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    current_level = [(start, [start])]
    next_level = []
    while current_level:
        (node, path) = current_level.pop()
        if node == goal:
            return path
        nodes = graph.get_connected_nodes(node)
        for n in nodes:
            if not filter(lambda x: x[0] == n, next_level) and not n in path:
                next_level.append((n, path + [n]))
        if not current_level:
             next_level = sorted(next_level, 
                    key = (lambda x: graph.get_heuristic(x[0], goal)))[0:beam_width]
             current_level = next_level
             next_level = []   
    return []

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    length = 0
    last_node = node_names[0]
    for node in node_names[1:]:
        length += graph.get_edge(last_node, node).length
        last_node = node
    return length


def branch_and_bound(graph, start, goal):
    agenda = [(start, [start], 0)]
    while agenda:
        (node, path, length) = agenda.pop()
        if node == goal:
            return path
        nodes = graph.get_connected_nodes(node)
        for n in nodes:
            if not n in path:
                agenda.append((n, path + [n], 
                        path_length(graph, path + [n])))
        agenda = sorted(agenda, key = lambda n: n[2], reverse=True)
    return []

def a_star(graph, start, goal):
    visited, agenda = set(), [(start, [start], 0)]
    while agenda:
        (node, path, length) = agenda.pop()
        if node == goal:
            return path
        visited.add(node)
        nodes = graph.get_connected_nodes(node)
        for n in nodes:
            if not n in visited:
                agenda.append((n, path + [n], path_length(graph, path + [n])))
        agenda = sorted(agenda, key=lambda n: n[2] + graph.get_heuristic(n[0], goal), reverse=True)
    return []


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    visited, agenda = set(), [(goal, [goal], 0)]
    while agenda:
        (node, path, length) = agenda.pop()
        if graph.get_heuristic(node, goal) > length:
            return False
        visited.add(node)
        nodes = graph.get_connected_nodes(node)
        for n in nodes:
            if not n in visited:
                agenda.append((n, path + [n], path_length(graph, path + [n])))
        agenda = sorted(agenda, key = lambda n: n[2], reverse=True)
    return True

def is_consistent(graph, goal):
    visited, agenda = set(), [goal]
    while agenda:
        node = agenda.pop()
        visited.add(node)
        nodes = graph.get_connected_nodes(node)
        for n in nodes:
            if not n in visited:
                agenda.append(n)
                if abs(graph.get_heuristic(node, goal) - graph.get_heuristic(n, goal)) > path_length(graph, [n, node]):
                    return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '3'
WHAT_I_FOUND_INTERESTING = '45'
WHAT_I_FOUND_BORING = '65'
