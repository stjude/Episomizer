#!/usr/bin/env python3
"""
Python version: 3.6
Author: Liang Ding
Date: 8/9/2017

Find simple cycles for a undirected graph.
Different with version 1, this version uses two vertices to represent a segment.
"""

import networkx as nx


def find_simple_cycles(dg):
    """ Find all simple cycles of a networkx graph.
        Args:
            dg (obj): a networkx graph
        Return:
            simple_cycles (list): a list of all simple cycles.
    """
    simple_cycles = [c for c in nx.simple_cycles(dg) if len(c) > 2]
    simple_cycles.sort(key=lambda cycle: len(cycle), reverse=True)
    return simple_cycles


def print_simple_cycles(simple_cycles):
    """ Print simple cycles.
        Args:
            simple_cycles (list): a list of lists
        Returns:
            None
    """
    print('Number of simple cycles: ' + str(len(simple_cycles)))
    for c in simple_cycles:
        print(c)
    print('\n')
    return


def print_simple_cycle(graph, sp):
    """ Print a simple cycle.
    Args:
        graph (obj): a networkx graph
        sp (list): a simple cycle
    Returns:
        None
    """
    if sp[0][:-1] == sp[1][:-1]:    # First two nodes form a segment edge
        first_node = sp.pop(0)
        sp.append(first_node)
    in_segment = False
    for index, node in enumerate(sp[:-1]):
        if in_segment:
            print(node[-1], end='')
        else:
            print(node, end='')
        if node[:-1] == sp[index+1][:-1]:
            print('', end='')       # segment edge
            in_segment = True       # next node is in segment
        else:
            print(' -', end='')     # non-segment edge
            print(graph[node][sp[index+1]]['type'][0].lower(), end='')
            print('-> ', end='')
            in_segment = False      # next node is not in segment
    if sp[-1][:-1] == sp[-2][:-1]:
        print(sp[-1][-1] + '\n')
    else:
        print(sp[-1] + '\n')
    return


def cycle_cover(cycles):
    """ Given all simple cycles, get a set of cycles that covers all segments.
    Args:
        cycles (list): all simple cycles.
    """

    return


def main():
    return


if __name__ == '__main__':
    main()
