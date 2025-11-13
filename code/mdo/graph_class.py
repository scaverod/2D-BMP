"""
    graph.py
"""

import math

from typing import List
from dataclasses import dataclass, field
from abc import abstractmethod



@dataclass(frozen=False)
class BandwidthParameters:
    """ given parameters (arguments) in a bandwidth calculation """
    k:int  = field(default=None)
    lb:int = field(default=None)
    ub:int = field(default=None)
    data:str = field(default=None)

    def __post_init__(self):
        if self.k is not None:
            self.lb = self.k
            self.ub = self.k + 1



@dataclass(frozen=False)
class BandwidthSolution:
    """ solution found in a bandwidth computation """
    status:str    = field(default="UNSAT")
    k:int         = field(default=None)
    solution:list = field(default=None)




# ============ GraphCB ================


class GraphCB:
    """
        A graph for 2D-bandwidth computation
        Nodes are numbered starting from 1 (and not zero)

        @l_neighbors : A list of n neighbors for node v
        tlb, tub : Theoretical bounds for a given bandwidth [[k, (lb,ub)]]
    """

    # instance attributes
    instance_name: str
    n_vertices   : int
    n_edges      : int
    l_edges      : List[List[int]]
    # computed attributes for this instance
    tlb       :int
    tub       :int
    grid_size :int
    # others
    l_neighbors : []


    def __init__(self, name:str, n_vertices: int, n_edges: int, graph: List[List[int]], tr):
        """ constructor """
        self.instance_name = name
        self.n_vertices = n_vertices
        self.n_edges = n_edges
        self.l_edges = graph
        self.l_neighbors = []
        self.l_triangles = list()
        self.generate_neighbors()
        self.grid_size = math.ceil(math.sqrt(self.n_vertices))


    def __str__(self) -> str:
        txt = f"""
            Instance: {self.instance_name}\n
            {self.n_vertices} vertices
            {self.n_edges} edges\n"""
            # Edges:\n{*self.l_edges,}\n
            # Neighbors (vertex, #neighbors, neighbors_list):\n
            # """
        return txt.replace("  ", '')

    @abstractmethod
    def generate_valid_labels(self, k: int):
        """ generate valid labels()
            It can be node or edge labels, depending on the problem.
        """


    @abstractmethod
    def calculate_theoretical_bounds(self):
        """ calculate theo bounds """


    # def generate_triangles(self) -> None:
    #     """
    #     generate triangles, i.e., cycles of size 3 of the graph
    #     triangles are of the form [v1,v2,v3] with v1<v2<v3
    #     """
    #     self.l_triangles = [[x, y, z] for [x, y] in self.l_edges for [y1, z] in self.l_edges \
    #         for [x1, z1] in self.l_edges if x == x1 and y == y1 and z == z1]


    # def generate_neighbors(self, graph: List[List[int]]) -> None:
    def generate_neighbors(self) -> None:
        """
        Get neighbors list for each vertex: 
            list, l_neighbors[v-1]=[v,n,[v1,...,vn]] for each vertex v, 
        meaning,
            v has n neighbors v1, ..., vn.
            vi are numbered from 1 to n (not 0 to n-1)

        assumption: For all edge (a,b), a<b
        """

        self.l_neighbors = []

        # for each  node, create an empty container
        for i in range(self.n_vertices):
            self.l_neighbors.append([i + 1, 0, []])

        # fill the container with node_id, nb_neighbors, neighbors
        # TODO : try a list comprehension --> for i in range(1,3): [b for a,b in edges if a==i]
        for a,b in self.l_edges:
            self.l_neighbors[a-1][1] = self.l_neighbors[a-1][1] + 1
            self.l_neighbors[a-1][2].append(b)

            self.l_neighbors[b-1][1] = self.l_neighbors[b-1][1] + 1
            self.l_neighbors[b-1][2].append(a)
        self.l_neighbors.sort(reverse=True, key=lambda x: x[1])
