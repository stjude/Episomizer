#!/usr/bin/env python
"""
Python version: 2.7.13
Author: Liang Ding
Date: 8/18/2017

This module constructs a networkx graph.
"""

import networkx as nx
import matplotlib.pyplot as plt


def build_graph(graph_text):
    """ Read a text file with number of nodes and edges. Create a networkx bidirectional graph.
        Args:
            graph_text (str): a text file with the first line number of vertices. The rest
            of lines are edges with one edge per line.
        Return:
            A networkx graph object.
    """
    # Read graph text file
    edge_lst = []
    with open(graph_text, 'r') as fin:
        num_vertices = int(fin.readline().rstrip())
        while True:
            line = fin.readline().rstrip()
            if not line:
                break
            edge_lst.append(tuple([ v for v in line.split('\t')]))

    # Create networkx graph object
    dg = nx.DiGraph()
    # Add two nodes for every segment; add segment edges
    for i in range(0, num_vertices):
        dg.add_node(str(i+1) + 'L')
        dg.add_node(str(i+1) + 'R')
        dg.add_edge(str(i+1) + 'L', str(i+1) + 'R')
        dg.add_edge(str(i+1) + 'R', str(i+1) + 'L')
    # Add non-segment edges
    for e in edge_lst:
        dg.add_edge(e[0], e[1])
        dg.add_edge(e[1], e[0])
    return dg


def print_graph(graph, verbose):
    """ Print a networkx graph.
    Args:
        graph (object): a networkx graph
        verbose (bool): whether to print nodes and edges
    Return:
        None
    """
    print('Number of vertices: ' + str(len(graph.nodes())))
    if verbose:
        print(graph.nodes())
        print('\n')
    print('Number of edges: ' + str(len(graph.edges())))
    if verbose:
        print(graph.edges())
        print('\n')
    return


def draw_graph(graph):
    """ Draw networkx graph with Matplotlib.
    Args:
        graph (object): a networkx graph.
    Return:
        None
    """
    #nx.draw(graph)
    nx.draw_circular(graph)
    #nx.draw_spectral(graph)
    plt.show()
    return





def main():
    return


if __name__ == '__main__':
    main()
