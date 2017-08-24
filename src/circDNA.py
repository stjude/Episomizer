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
    circRNA()
    return


def circRNA():
    """ Driver function to detect circular DNA.
        Returns:
            None
    """
    graph_text = '../inputs/edges_for_graph_S_full_no_chromium.txt'
    dg = graph.build_graph(graph_text)
    graph.to_sig(dg)
    #graph.draw_graph(dg)

    # Find all simple cycles
    simple_cycles = cycle.find_simple_cycles(dg)
    filtered_scs = path.filter_jump_paths(simple_cycles)
    #for sc in filtered_scs:
    #    path.draw_simple_path(dg, sc)
    #print()

    # Find all dangling nodes
    dangling_nodes = graph.find_dangling_nodes(dg)
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
