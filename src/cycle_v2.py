#!/usr/bin/env python
"""
Python version: 2.7.13
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
            A list of all simple cycles.
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


def main():
    return


if __name__ == '__main__':
    main()
