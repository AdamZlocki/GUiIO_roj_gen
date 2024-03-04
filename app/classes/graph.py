from typing import List

from app.classes.edge import Edge
from app.classes.vertex import Vertex


class GraphMatrix:
    """Graf - jak na labach Pawlika składa się z listy wierzhcołków, macierzy krawędzi i słownika"""
    def __init__(self):
        self.list: List[Vertex] = []
        self.dict = {}
        self.matrix: List[List[Edge or int]] = [[]]

    def insert_vertex(self, vertex: Vertex):
        self.list.append(vertex)
        self.dict[vertex] = self.order() - 1
        if self.order() != 1:
            for i in range(len(self.matrix)):
                self.matrix[i].append(0)
            self.matrix.append([0] * len(self.matrix[0]))
        else:
            self.matrix[0].append(0)

    def insert_edge(self, vertex1_idx: int, vertex2_idx: int, edge: Edge):
        if vertex1_idx is not None and vertex2_idx is not None and edge is not None:
            self.matrix[vertex1_idx][vertex2_idx] = edge

    # def deleteVertex(self, vertex):
    #     vertex_idx = self.getVertexIdx(vertex)
    #     for i in range(self.order()):
    #         if i != vertex_idx:
    #             self.matrix[i].pop(vertex_idx)
    #     self.matrix.pop(vertex_idx)
    #     self.list.pop(vertex_idx)
    #     self.dict.pop(vertex)
    #     for i in range(vertex_idx, self.order()):
    #         actual = self.list[i]
    #         self.dict[actual] -= 1
    #
    # def deleteEdge(self, vertex1, vertex2):
    #     vertex1_idx = self.getVertexIdx(vertex1)
    #     vertex2_idx = self.getVertexIdx(vertex2)
    #     for i in range(len(self.matrix[vertex1_idx])):
    #         if self.matrix[vertex1_idx][vertex2_idx] != 0:
    #             self.matrix[vertex1_idx][vertex2_idx] = 0

    def get_vertex_idx(self, vertex):
        return self.dict[vertex]

    def get_vertex(self, vertex_idx) -> Vertex:
        return self.list[vertex_idx]

    def neighbours(self, vertex_idx) -> List[int]:  # zwraca indeksy w macierzy sąsiadów wybranego wierzchołka
        result = []
        for i in range(len(self.matrix[vertex_idx])):
            if self.matrix[vertex_idx][i]:
                result.append(i)
        return result

    def order(self):
        return len(self.list)

    def size(self):
        result = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] != 0:
                    result += 1
        return result

    def edges(self):
        result = []
        for i in range(self.order()):
            for j in range(self.order()):
                if self.matrix[i][j]:
                    result.append(self.matrix[i][j])
        return result

    def reset_visited(self):
        for vertex in self.list[1:]:
            vertex.visited = 0
