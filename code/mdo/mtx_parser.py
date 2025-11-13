"""
    mtx_parser.py
    Reads a graph in MatrixMarket "coordinates" format. 
"""

import re
from pycsp3.problems.data.parsing import data, remaining_lines, numbers_in

n_nodes:int = 0
n_edges:int = 0
edges = []

for line in remaining_lines(skip_curr=False):
    if line.startswith(("%","#")):
        # comments
        continue

    if n_nodes * n_edges == 0:
        # row/cols number should be placed before edge info
        if re.search("^([0-9]+ [0-9]+)$",line):
            n_nodes, n_edges = numbers_in(line)
        elif re.search("^([0-9]+ [0-9]+ [0-9]+)$",line):
            _, n_nodes, n_edges = numbers_in(line)
    else:
        # edges
        a,b = numbers_in(line)
        edges.append(sorted([a,b]))

# check: an instance should have (at least) one edge
assert len(edges) > 0

# return values to main program
data["n_vertices"] = n_nodes
data["n_edges"]    = n_edges
data["edges"]      = sorted(edges)
