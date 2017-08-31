#!/usr/bin/env python
"""
Python version: 2.7.13
Note: this is written to be compatible with python3. But networkx draw does not support
python3 very well. Suggest running in python2.

Author: Liang Ding
Date: 8/18/2017

Circular DNA detector.
"""

import itertools

import graph
import cycle_v2 as cycle
import path


def main():
    """ Program gate and argument handler.
    """
    #circRNA()
    linearRNA()
    return


def circRNA():
    """ Driver function to detect circular DNA.
    """
    non_segment_file = '../inputs/edges_for_graph_E.txt'
    segment_file = '../inputs/edges_for_graph_E_segments.txt'
    dg = graph.build_graph(non_segment_file, segment_file)
    sif_file = '../outputs/edges_for_graph_E.sif'
    graph.to_sif(dg, sif_file)
    #graph.draw_graph(dg)
    find_circ_DNA(dg)
    return


def linearRNA():
    """ Driver function to detect linear DNA.
    """
    non_segment_file = '../inputs/edges_for_graph_E_linear.txt'
    segment_file = '../inputs/edges_for_graph_E_segments_linear.txt'
    dg = graph.build_graph(non_segment_file, segment_file)
    sif_file = '../outputs/edges_for_graph_E.sif'
    graph.to_sif(dg, sif_file)
    find_linear_DNA(dg)
    return


def find_circ_DNA(dg):
    """ Find and print all circular DNAs
    Args:
        dg (obj): a networkx directed graph object
    Returns:
        List: a list of circular DNAs
    """
    simple_cycles = cycle.find_simple_cycles(dg)
    filtered_scs = path.filter_jump_paths(simple_cycles)
    left_scs = path.rm_reverse_paths(filtered_scs)
    print('Number of cycles: ' + str(len(left_scs)))
    for sc in left_scs:
        path.draw_simple_path(dg, sc)
    return left_scs


def find_linear_DNA(dg):
    """ Find and print all linear DNAs
    Args:
        dg (obj): a networkx directed graph object
    Returns:
        List: a list of linear DNAs
    """
    # Find all dangling nodes
    dangling_nodes = graph.find_dangling_nodes(dg)
    dangling_nodes.append('5L')
    print('Dangling nodes: ', end='')
    for node in dangling_nodes:
        print(node + ' ', end='')
    print()

    # Find all simple paths from a source to a destination
    for n_pair in itertools.combinations(dangling_nodes, 2):
        print('s: ' + n_pair[0] + '\td: ' + n_pair[1])
        simple_paths = path.find_simple_paths(dg, n_pair[0], n_pair[1])
        filtered_sps = path.filter_jump_paths(simple_paths)
        for sp in filtered_sps:
            path.draw_simple_path(dg, sp)
    return


if __name__ == '__main__':
    main()
