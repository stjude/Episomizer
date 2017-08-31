#!/usr/bin/env python
"""
Python version: 2.7.13
Author: Liang Ding
Date: 8/18/2017

This module constructs a networkx graph.
"""

import networkx as nx
import matplotlib.pyplot as plt


def build_graph(non_segment_file, segment_file):
    """ Read a text file with number of nodes and edges. Create a networkx bidirectional graph.
        Args:
            graph_text (str): a text file with the first line number of vertices. The rest
            of lines are edges with one edge per line.
        Return:
            A networkx graph object.
    """
    # Read graph text file
    non_segment_edges = []
    with open(non_segment_file, 'r') as fin:
        while True:
            line = fin.readline().rstrip()
            if not line:
                break
            non_segment_edges.append(tuple([v for v in line.split('\t')]))

    # Create networkx graph object
    dg = nx.DiGraph()
    # Add two nodes for every segment; add segment edges
    with open(segment_file, 'r') as fin:
        while True:
            line = fin.readline().rstrip()
            if not line:
                break
            tokens = line.split('\t')
            dg.add_node(tokens[0])
            dg.add_node(tokens[1])
            dg.add_edge(tokens[0], tokens[1], type='segment')
            dg.add_edge(tokens[1], tokens[0], type='segment')

    # Add non-segment edges
    for e in non_segment_edges:
        dg.add_edge(e[0], e[1], type=e[5])
        dg.add_edge(e[1], e[0], type=e[5])
    return dg


def to_sif(graph, sif_file):
    """ Convert networkx graph to sig format.
    Args:
        graph (obj): a networkx graph object
    Return:
        A sig file
    """
    edge_set = set()
    with open(sif_file, 'w') as fout:
        for e in graph.edges(data='type'):
            edge_str = e[0] + ' ' + e[2] + ' ' + e[1]
            if edge_str not in edge_set:
                fout.write(edge_str + '\n')
            edge_set.add(edge_str)
            reverse_edge_str = e[1] + ' ' + e[2] + ' ' + e[0]
            edge_set.add(reverse_edge_str)
    return


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


def find_dangling_nodes(graph):
    """ Find nodes that have only segment edges.
    Args:
        graph (obj): a networkx graph object
    Returns:
        a list of dangling nodes
    """
    dangling_lst = []
    for node in graph.nodes():
        if len(graph[node]) == 1:   # nodes with only one edge (must be segment)
            dangling_lst.append(node)
        #elif len(graph[node]) == 2: # nodes with
        #    for pair_node in graph[node]:
        #        if(graph[node][pair_node]['type']) == 'adjacent':
        #            dangling_lst.append(node)
    return dangling_lst


def main():
    return


if __name__ == '__main__':
    main()
