#!/usr/bin/env python3
"""
This module contains functions to work with networkx graphs.
"""

import networkx as nx


def build_graph(cna_segment_file, linked_sv_file, **kwargs):
    """ Read a text file with number of nodes and edges. Create a networkx bidirectional graph.
    Args:
        Required arguments:
            cna_segment_file (str): path to a bed file containing somatic copy number alteration segments
            linked_sv_file (str): path to a tab-delimited text file containing linked structure variant boundaries
        optional keyword arguments:
            segment_attribute_file (str): path to a file with additional attributes of the segments
            (e.g., LogRatios, lengths, etc.)
    Return:
        obj: a networkx graph object.
            (edge attribute: type; segment edge attributes: Length and LogRatio)
    """
    # Read graph text file
    non_segment_edges = []
    with open(linked_sv_file, 'r') as fin:
        while True:
            line = fin.readline().rstrip()
            if not line:
                break
            non_segment_edges.append(tuple([v for v in line.split('\t')]))

    # Create networkx graph object
    dg = nx.DiGraph()

    # Add two nodes for every segment; add segment edges
    with open(cna_segment_file, 'r') as fin:
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

    if 'segment_attribute_file' in kwargs:
        with open(kwargs['segment_attribute_file']) as fin:
            fin.readline()
            while True:
                line = fin.readline().rstrip()
                if not line:
                    break
                tokens = line.split('\t')
                segment = tokens[0]
                log_ratio = float(tokens[2])
                length = int(tokens[3])
                dg[segment + 'L'][segment + 'R']['LogRatio'] = log_ratio
                dg[segment + 'R'][segment + 'L']['LogRatio'] = log_ratio
                dg[segment + 'L'][segment + 'R']['Length'] = length
                dg[segment + 'R'][segment + 'L']['Length'] = length
    return dg


def to_sif(graph, sif_file):
    """ Output a networkx directed graph object to a sig file.
    Args:
        graph (obj): a networkx directed graph object
        sif_file (str): path to an output sif file
    Return:
        None
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


def print_graph(graph, verbose):
    """ Print a networkx directed graph object.
    Args:
        graph (object): a networkx directed graph object
        verbose (bool): whether to print nodes and edges
    Return:
        None
    """
    print('Number of vertices: {}'.format(str(len(graph.nodes()))))
    if verbose:
        print(graph.nodes())
        print('\n')
    print('Number of edges: {}'.format(str(len(graph.edges()))))
    if verbose:
        print(graph.edges())
        print('\n')
