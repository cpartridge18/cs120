from itertools import product, combinations

'''
Before you start: Read the README and the Graph implementation below.
'''

class Graph:
    '''
    A graph data structure with number of nodes N, list of sets of edges, and a list of color labels.

    Nodes and colors are both 0-indexed.
    For a given node u, its edges are located at self.edges[u] and its color is self.color[u].
    '''

    # Initializes the number of nodes, sets of edges for each node, and colors
    def __init__(self, N, edges = None, colors = None):
        self.N = N
        self.edges = [set(lst) for lst in edges] if edges is not None else [set() for _ in range(N)]
        self.colors = [c for c in colors] if colors is not None else [None for _ in range(N)]
    
    # Adds a node to the end of the list
    # Returns resulting graph
    def add_node(self):
        self.N += 1
        self.edges.append(set())
        return self
    
    # Adds an undirected edge from u to v
    # Returns resulting graph
    def add_edge(self, u, v):
        assert(v not in self.edges[u])
        assert(u not in self.edges[v])
        self.edges[u].add(v)
        self.edges[v].add(u)
        return self

    # Removes the undirected edge from u to v
    # Returns resulting graph
    def remove_edge(self, u, v):
        assert(v in self.edges[u])
        assert(u in self.edges[v])
        self.edges[u].remove(v)
        self.edges[v].remove(u)
        return self

    # Resets all colors to None
    # Returns resulting graph
    def reset_colors(self):
        self.colors = [None for _ in range(self.N)]
        return self

    def clone(self):
        return Graph(self.N, self.edges, self.colors)

    def clone_and_merge(self, g2, g1u, g2v):
        '''
        DOES NOT COPY COLORS
        '''
        g1 = self
        edges = g1.edges + [[v + g1.N for v in u_list] for u_list in g2.edges]
        g = Graph(g1.N + g2.N, edges)
        if g1u is not None and g2v is not None:
            g = g.add_edge(g1u, g2v + g1.N)
        return g

    # Checks all colors
    def is_graph_coloring_valid(self):
        for u in range(self.N):
            for v in self.edges[u]:

                # Check if every one has a coloring
                if self.colors[u] is None or self.colors[v] is None:
                    return False

                # Make sure colors on each edge are different
                if self.colors[u] == self.colors[v]:
                    return False
        
        return True

'''
    Introduction: We've implemented exhaustive search for you below.

    You don't need to implement any extra code for this part.
'''

# Given an instance of the Graph class G, exhaustively search for a k-coloring
# Returns the coloring list if one exists, None otherwise.
def exhaustive_search_coloring(G, k=3):

    # Iterate through every possible coloring of nodes
    for coloring in product(range(0,k), repeat=G.N):
        G.colors = list(coloring)
        if G.is_graph_coloring_valid():
            return G.colors

    # If no valid coloring found, reset colors and return None
    G.reset_colors()
    return None


'''
    Part A: Implement two coloring via breadth-first search.

    Hint: You will need to adapt the given BFS pseudocode so that it works on all graphs,
    regardless of whether they are connected.

    When you're finished, check your work by running python3 -m ps5_color_tests 2.
'''

# Given an instance of the Graph class G and a subset of precolored nodes,
# Assigns precolored nodes to have color 2, and attempts to color the rest using colors 0 and 1.
# Precondition: Assumes that the precolored_nodes form an independent set.
# If successful, modifies G.colors and returns the coloring.
# If no coloring is possible, resets all of G's colors to None and returns None.
def bfs_2_coloring(G, precolored_nodes=None):
    # Assign every precolored node to have color 2
    # Initialize visited set to contain precolored nodes if they exist
    # print(G.edges)
    # print(G.colors)

    # unvisited = clone(G)  # Create a new graph for tracking unvisited nodes

    visited = set()  #S
    G.reset_colors()
    preset_color = 2
    if precolored_nodes is not None:
        for node in precolored_nodes:

            # unvisited.remove_edge(node)

            G.colors[node] = preset_color
            visited.add(node)

        if len(precolored_nodes) == G.N:
            return G.colors


    # Start with breadth-first search to get ordering based on distance to start node
    if precolored_nodes is not None:
        for node in precolored_nodes:
            del G.edges[node] #remove all precolored edges

    order = {0:[0]} # order is a dictionary with distance from start vertex as key
                    #      and list of vertices in that frontier as value
    pre_order = []  # holding list for order dict
    F = [0]
    unvisited = list(range(1, G.N)) # we assume 0 was already visited
    # print(len(F))
    d = 1   # dictionary is autofilled with distance 0

    # runs until all nodes have been visited. 
    while unvisited:

        if not F:   # if frontier is empty but there are unvisited nodes, choose the first from the list. 
                    #   We will just add this to the dictionary as a distance 1 greater than the last 
                    #   connected component from the start vertex, when in reality distance is infinite.
            F = [unvisited[0]]

        pre_F = []
        pre_order = []        
        for f in F:               # for all vertices in the previous frontier
            for v in G.edges[f]:  # check their edges
                if v in unvisited: # if they haven't been visited
                    pre_order.append(v)   # add to pre_order list 
                    pre_F.append(v)       # add to pre_froniter list
                    unvisited.remove(v)    # add all nodes that share an edge

        if pre_order:
            order[d] = pre_order   # add to order
        F = pre_F   # update frontier
        d += 1

    # based on BFS ordering, color either 0 or 1    

    for distance in order: 
        if (distance % 2) == 0:
            color = 0
        else:
            color = 1

        for node in order[distance]:
            G.colors[node] = color

    # If G is disconnected, then run BFS on each connected component separately



    if G.is_graph_coloring_valid():
            return G.colors

    G.reset_colors()
    return None

'''
    Part B: Implement is_independent_set.
'''

# Given an instance of the Graph class G and a subset of precolored nodes,
# Checks if subset is an independent set in G 
def is_independent_set(G, subset):
    # TODO: Complete this function
    for u in subset:
        for v in G.edges(u):
            if v in subset:
                return False
    return True

'''
    Part C: Implement the 3-coloring algorithm from the sender receiver exercise.
    
    Make sure to call the bfs_2_coloring and is_independent_set functions that you already implemented!

    Hint 1: You will want to use the Python `combinations` function from the itertools library
    to enumerate all possible independent sets. Remember that each element of combinations is a tuple,
    so you may need to convert it to a list.

    Hint 2: Python itertools functions compute their results lazily, which means that they only
    calculate each element as the program requests it. This saves time and space, since it
    doesn't need to store the entire list of combinations up front. You should NOT try to convert the result
    of the entire combinations call to a list, since that will force Python to precompute everything.
    Instead, you should iterate over them in a for loop, which will maintain the lazy behavior we want.
    See the call to "product" in exhaustive_search for an example.

    When you're finished, check your work by running python3 -m ps5_color_tests 3.
    Don't worry if some of your tests time out: that is expected.
'''

# Given an instance of the Graph class G (which has a subset of precolored nodes), searches for a 3 coloring
# If successful, modifies G.colors and returns the coloring.
# If no coloring is possible, resets all of G's colors to None and returns None.
def iset_bfs_3_coloring(G):
    # TODO: Complete this function.
    # create all subsets of G's vertices less than or equal to G.N/3

    # mother of god this is even worse than 1a what are you doing
    #  you have so many for loops you could for-get about getting full credit

    G_clone = G.clone
    subsets = []
    for u in range((int)(G.N/3)):                           # for all numbers between 1 and G.N/3
        for subset in combinations(list(range(G.N)), u):    # for all subsets of size u
            if is_independent_set(G,subset):                # checks if it is independent
                for i in subset:                            # if so, removes edge from copy of G, creating G - S
                    for j in G_clone.edges(i):
                        G_clone.remove_edge(i,j)

                f_s = bfs_2_coloring(G_clone)               # 2 color G - S
                if f_s:                                 
                    for k in range(G.N):                    # if successful, add old edges back in
                        if k not in G_clone.edges:          # if the node is not in 2colored subset (CHECK SYNTAX HERE)
                            for l in G.edges(k):            # , add it back and color it 2
                                G_clone.add_edge(k,l)
                                G_clone.colors[k] = 2
                    return G_clone.colors                   # return coloring
        #     print(subset)


    G.reset_colors()
    return None

# Feel free to add miscellaneous tests below!
if __name__ == "__main__":
    G0 = Graph(2).add_edge(0, 1)
    print(bfs_2_coloring(G0))
    print(iset_bfs_3_coloring(G0))
