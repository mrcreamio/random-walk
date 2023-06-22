import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

def random_walk_from_matrix(matrix, num_visits, start_node):
    # Ensure that the matrix is a 5x5 numpy array.
    if isinstance(matrix, list):
        matrix = np.array(matrix)
    assert matrix.shape == (5, 5), "Input matrix must be 5x5."

    # Create a directed graph from the matrix.
    G = nx.DiGraph(matrix)

    # Check if start_node is valid
    assert start_node in G.nodes, "Invalid start node."

    # Initiate a dictionary to keep track of visits.
    visit_counts = {node: 0 for node in G.nodes}

    # List to keep track of the path taken.
    path = []

    current_node = start_node
    for _ in range(num_visits):
        visit_counts[current_node] += 1
        path.append(current_node)
        neighbors = list(G.neighbors(current_node))
        if neighbors:
            current_node = random.choice(neighbors)
        else:
            break

    # Convert counts to percentages.
    visit_percentages = {node: count / num_visits * 100 for node, count in visit_counts.items()}

    return visit_percentages, path

# Streamlit code starts here
st.title("Random Walk on a Directed Graph")

# Take user inputs
num_visits = st.number_input("Number of nodes to visit:", min_value=1, value=10, step=1)
start_node = st.number_input("Starting node:", min_value=0, max_value=4, value=0, step=1)

# Define default matrix
default_matrix = [[0, 1, 0, 0, 1],
                  [0, 0, 1, 0, 0],
                  [1, 0, 0, 1, 0],
                  [0, 1, 0, 0, 1],
                  [1, 0, 1, 0, 0]]

# Take matrix input from user
matrix = st.text_area("Enter adjacency matrix as rows of numbers, separated by spaces. (5x5 matrix)", 
                      value='\n'.join(' '.join(str(x) for x in row) for row in default_matrix))
matrix = [[int(x) for x in row.split()] for row in matrix.split('\n')]
# Perform random walk
visit_percentages, path = random_walk_from_matrix(matrix, num_visits, start_node)

# Display visit percentages and path
st.subheader("Visit Percentages")
st.write(visit_percentages)
st.subheader("Path")
st.write(path)

# Create graph
G = nx.DiGraph(nx.convert_matrix.from_numpy_array(np.array(matrix)))
pos = nx.circular_layout(G)
fig, ax = plt.subplots()
nx.draw_networkx_nodes(G, pos, node_size=700, ax=ax)
nx.draw_networkx_labels(G, pos, ax=ax)
nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20, ax=ax)

# Highlight path
if path:
    edges = [(path[i-1], path[i]) for i in range(1, len(path))]
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='r', width=2, arrowstyle='-|>', arrowsize=20, ax=ax)

st.pyplot(fig)