#!/usr/bin/env python
"""
Python version: 2.7.13
Note: this is written to be compatible with python3. But networkx draw does not support
python3 very well. Suggest running in python2.

Author: Liang Ding
Date: 8/18/2017

Circular DNA detector.
"""

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
    graph_text = '../inputs/edges_for_graph_S.txt'
    dg = graph.build_graph(graph_text)
    #graph.draw_graph(dg)
    simple_cycles = cycle.find_simple_cycles(dg)
    filtered_scs = path.filter_jump_paths(simple_cycles)
    for sc in filtered_scs:
        print(sc)
    print

    s_node = '6L'
    t_node = '7L'
    simple_paths = path.find_simple_paths(dg, s_node, t_node)
    filtered_sps = path.filter_jump_paths(simple_paths)
    for sp in filtered_sps:
        print(sp)
    return


if __name__ == '__main__':
    main()
