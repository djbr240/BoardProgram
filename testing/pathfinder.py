def find_reachable_spaces(graph, start_node, roll_number):
    visited = set()  # To avoid revisiting nodes
    queue = [(start_node, 0)]  # Use a queue for BFS, storing (node, depth)
    
    reachable = []  # List to store reachable nodes
    
    while queue:
        current, depth = queue.pop(0)  # Dequeue
        if current not in visited:
            visited.add(current)
            if depth <= roll_number:
                reachable.append(current)
                # Add neighbors to the queue with incremented depth
                queue.extend((neighbor, depth + 1) for neighbor in graph.get(current, []))
    
    return reachable

# Define your graph
graph = {
    0: [10],
    1: [9],
    2: [3, 8],
    3: [2, 8],
    4: [7],
    5: [6],
    6: [5, 7],
    7: [4, 6, 8, 15],
    8: [2, 3, 7, 14],
    9: [14],
    10: [0, 11],
    11: [10, 13],
    12: [13],
    13: [11, 14, 20],
    14: [8, 9, 13, 15, 21],
    15: [7, 14, 16, 19],
    16: [15, 17],
    17: [16],
    18: [19, 28, 29],
    19: [15, 18, 27],
    20: [13, 21, 22, 23],
    21: [14, 20, 22, 25],
    22: [20, 21, 23],
    23: [20, 22],
    24: [25, 38],
    25: [21, 24, 26, 37],
    26: [25, 27],
    27: [19, 26, 28, 31, 33],
    28: [18, 27, 29],
    29: [18, 28],
    30: [31],
    31: [27, 33],
    32: [33],
    33: [27, 31, 32, 35],
    34: [35, 37],
    35: [33, 34, 36],
    36: [35, 37],
    37: [25, 34, 36],
    38: [24, 39],
    39: [38],
    40: [37],
    41: [33]
}

# Find reachable spaces from node 19 with roll number 2
reachable_spaces = find_reachable_spaces(graph, start_node=6, roll_number=2)
print("Reachable spaces:", reachable_spaces)
