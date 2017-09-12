#!/usr/bin/env python3
"""
Python version: 3.6
Author: Liang Ding
Date: 8/18/2017

This module constructs a networkx graph.
"""

import networkx as nx
import matplotlib.pyplot as plt


def build_graph(non_segment_file, segment_file):
    """ Read a text file with number of nodes and edges. Create a networkx bidirectional graph.
        Args:
            non_segment_file (str): a text file with non-segment edges.
            segment_file (str): a text file with segment edges.
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
            dg.add_edge(tokens[0], tokens[1], type='SEG')
            dg.add_edge(tokens[1], tokens[0], type='SEG')

    # Add non-segment edges. Use column 5 as edge type
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


def find_dangling_nodes(graph):
    """ Find dangling nodes from the graph. A dangling node in a graph is defined as:
        consider two nodes of a SEG edge
            (1) one node (dangling) only has SEG edge, other node has D/S/B/A/
                (basicly, other side does not have any constraint);
            (2) one node (dangling) only has SEG and adjacent edge, other side must have any
                of D/S/B edges.
    Args:
        graph (obj): a networkx graph object
    Returns:
        a list of dangling nodes
    """
    dangling_lst = []
    for node1 in graph.nodes():
        if len(graph[node1]) == 1:   # Nodes with only one edge (must be segment)
            dangling_lst.append(node1)
        elif len(graph[node1]) == 2: # Nodes with two edges (one segment edge and one adjacent)
            connect_nodes = list(graph[node1].keys())
            node2_1 = connect_nodes[0]
            node2_2 = connect_nodes[1]
            is_keep = False     # Keep nodes with a SEG edge and a A edge
            node2_seg = ''
            if graph[node1][node2_1]['type'] == 'SEG' or graph[node1][node2_2] == 'A':
                is_keep = True
                node2_seg = node2_1
            elif graph[node1][node2_2]['type'] == 'SEG' or graph[node1][node2_1] == 'A':
                is_keep = True
                node2_seg = node2_2
            if is_keep:
                edge_types = [list(edge_type.values())[0] for edge_type in graph[node2_seg].values()]
                desire_edges = ['D', 'S', 'B']
                # If edges of node2_seg contain one of D, S, B
                if len([e for e in desire_edges if e in edge_types]) > 0:
                    dangling_lst.append(node1)
    return dangling_lst


def main():
    return


if __name__ == '__main__':
    main()
