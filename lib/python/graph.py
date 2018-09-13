#!/usr/bin/env python3
"""
This module contains functions to work with networkx graphs.
"""

import networkx as nx
import pybedtools


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
    linked_sv_edges = []
    with open(linked_sv_file, 'r') as fin:
        while True:
            line = fin.readline().rstrip()
            if not line:
                break
            linked_sv_edges.append(tuple([v for v in line.split('\t')]))

    # Create networkx graph object
    dg = nx.DiGraph()

    # Add two nodes for every segment; add segment edges
    cna_segments = pybedtools.BedTool(cna_segment_file)
    for segment in cna_segments:
        node_name1 = '{}L'.format(segment[3])
        node_name2 = '{}R'.format(segment[3])
        dg.add_node(node_name1)
        dg.add_node(node_name2)
        dg.add_edge(node_name1, node_name2, type='SEG')
        dg.add_edge(node_name2, node_name1, type='SEG')
        length = int(segment[2]) - int(segment[1])
        dg[node_name1][node_name2]['Length'] = length
        dg[node_name2][node_name1]['Length'] = length

    # Add non-segment edges. Use column 5 as edge type
    for e in linked_sv_edges:
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
