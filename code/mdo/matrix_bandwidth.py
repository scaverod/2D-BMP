"""
    matrix_bandwidth.py
    Solves a 2d-bandwidth constraint model

    __author__     = "Eric Monfroy"
    __copyright__  = "Copyright 2024"
    __license__    = "GPL"
    __version__    = "0.1"
    __maintainer__ = "Eric Monfroy, Claudia Vasconcellos-Gaete"
    __email__      = "{eric.monfroy,claudia.vasconcellos}@univ-angers.fr"
    __status__     = "Development"

    Usage :
        python3 matrix_bandwidth.py -k=<K> -data=<instance> -dataparser=mtx_parser.py
        python3 matrix_bandwidth.py -lb=<LB> -ub=<UB> -data=<instance> -dataparser=mtx_parser.py
"""

import sys
import math
import time

from typing import List
from graph_class import GraphCB, BandwidthParameters
from pycsp3 import * 
# from icecream import ic # debugging




class MatrixBandwidthGraph(GraphCB):
    """ MatrixBandwidthGraph class """
    def __init__(self, name, nb_nodes, nb_edges, edges):
        super().__init__(name, nb_nodes, nb_edges, edges, False)
        self.calculate_theoretical_bounds()

    def calculate_theoretical_bounds(self):
        """ theoretical bounds for the 2d-bandwidth """
        d: int   = self.l_neighbors[0][1]
        tlb: int = 0
        self.tub = self.grid_size

        while d > 0:
            tlb += 1
            d = d - tlb*8

        self.tlb = tlb


    def generate_valid_labels(self, k: int):
        """
            V4
            k: int -- Bandwidth value

            Generate all valid labels for edges, based on 
            the $DL_{inf}$ norm (Lin2010).
            
            This distance does not mean the length of wire connecting 
            points (i,j) and (i',j'), but may represent the "dilation" 
            along the vertical and horizontal directions.

            dlinf((i,j)(i',j')) = max{|i-i'|,|j-j'|}

            The output ("labels") contains all the valid edges (ax,bx) 
            for a host graph G'(V',E'), IN A SINGLE AXIS. 

        """

        grid: int = self.grid_size
        labels: List = []

        for i1 in range(1, grid+1):
            for i2 in range(1, grid+1):
                if abs(i2-i1) <= k :
                    labels.append((i1,i2))

        return labels



# Fin de la classe MatrixBandwidthGraph -------------------------


def read_parameters() -> BandwidthParameters:
    """ Reads parameters from command-line. 
        (skips argv[0], aka the script name)
    """
    parameters = BandwidthParameters()

    for arg in sys.argv[1:]:
        if '=' not in arg:
            sys.exit(0)

        key:str = arg.split('=', maxsplit=1)[0].replace('-', '')
        val:str = arg.split('=', maxsplit=1)[1].strip()

        if key == "k":
            parameters.k = int(val)
        elif key == "lb":
            parameters.lb = int(val)
        elif key == "ub":
            parameters.ub = int(val)
        elif key == "data":
            parameters.data = val.replace(".rnd","").replace(".mtx","")

    return parameters



def solve_mbmp(graph: GraphCB, bandwidth: int) -> dict:
    """ 
        Solves the 2d-bandwidth problem using constraints.

        Parameters: 
        graph (GraphCB): A graph instance
        bandwidth (int): 2D-bandwidth value to test

        Decision vars (or, the grid labels) are in the form of 
        list of pairs, where:
            labels[i]=[l1,l2] <=> (l1,l2) is the label for the ith-node

        Search space:
        All the possible edge labels for a given grid
    """
    start_time = time.time()

    # graph/grid size
    n: int = graph.n_vertices
    grid_size: int = graph.grid_size
    edges = graph.l_edges

    # Decision vars (a grid of..)
    labels = VarArray(size=[n,2], dom=range(1, grid_size+1))


    satisfy(
        # C1: Each label is different
        AllDifferent(x*(grid_size+1) + y for x,y in labels)
    )

    # C2: Symmetry breaking
    # fix the label of the maximum degree node (dmax) to be in the first half cuadrant
    # (dmax is adjusted for Python's array indexing)
    dmax: int = graph.l_neighbors[0][0] - 1

    satisfy(
        labels[dmax][0] <= int(math.ceil(grid_size/2)),
        labels[dmax][1] <= int(math.ceil(grid_size/2)),
        labels[dmax][1] <= labels[dmax][0]
    )

    # C3: Enforce labels to be correct
    search_space = graph.generate_valid_labels(bandwidth)

    # C3a
    satisfy(
        # enforce x-labels of edges to be correct
        [(labels[a-1][0], labels[b-1][0]) in search_space for a,b in edges]
    )
    satisfy(
        # enforce y-labels of edges to be correct
        [(labels[a-1][1], labels[b-1][1]) in search_space for a,b in edges]
    )

    # build results
    result = {
        'status': "UNSAT",
        'solution': None,
        'ext_table_size': len(search_space)
    }
    if solve(solver=CHOCO) is SAT:
        result['status']   = "SAT"
        result['solution'] = [ values(labels[i]) for i in range(n) ]

    end_time = time.time()
    result['runtime'] = end_time - start_time

    # clear every variable and constraint posted
    unpost(ALL)
    clear()
    return result



def main() -> None:
    """ main function 
        * note that pycsp invokes the data parser before anything happens
    """

    start_time = time.time()
    args = read_parameters()

    # graph
    _nbnodes, _nbedges, _edges = list(data)
    instance = MatrixBandwidthGraph(
        name     = args.data,
        nb_nodes = _nbnodes,
        nb_edges = _nbedges,
        edges    = [ [a,b] for (a,b) in _edges ] # to force a type casting
    )
    print(instance)

    # shortening bounds
    lb:int = max(args.lb, instance.tlb)
    ub:int = min(args.ub, instance.tub)
    print(f"bounds after shortening: [{lb},{ub}]", end="\n\n")

    # calculations
    while True:
        print(f"[{lb},{ub}]", end='\t')
        k:int = (lb+ub) // 2
        result = solve_mbmp(instance, bandwidth=k)

        print(f"(trying)\tk={k}", end='\t')
        print(f"{result['status']}", end='\t')
        print(f"runtime={(result['runtime']):.2f}", end='\t')
        print(f"ext={result['ext_table_size']}", end='\t')
        print(f"grid={instance.grid_size}", end='\t')
        print(f"sol={result['solution']}")

        if result['status'] == "SAT":
            ub = k-1
        else:
            lb = k+1

        if lb > ub :
            break


    end_time = time.time()
    print()
    print(f"""start time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))}""")
    print(f"""end time  : {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))}""")
    print(f"({(end_time-start_time):.2f} secs)", end='\n\n')



if __name__ == '__main__':
    main()
