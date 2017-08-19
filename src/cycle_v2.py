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


def filter_jump_cycle(simple_cycles):
    """ Filter jump simple cycles.
        Args:
            simple_cycles (list): a list of simple cycles
        Return:
            a list of filtered simple cycles
    """
    filter_scs = []
    for sc in simple_cycles:
        valid_sc = True
        node_counter = dict()
        for i in range(0, len(sc)-2):
            node1 = int(sc[i][:-1])
            node2 = int(sc[i + 1][:-1])
            node3 = int(sc[i + 2][:-1])
            # Filter jump in the middle of a simple cycle
            # There should not be 3 consecutive different nodes
            if node1 != node2 and node2 != node3:
                valid_sc = False
                break
         
        # Filter jump at the end of a sc
        first = int(sc[0][:-1])
        second = int(sc[1][:-1])
        last = int(sc[-1][:-1])
        second_last = int(sc[-2][:-1])
        if last == second_last:
            if first != second:
                valid_sc = False
        else:
            if first != last:
                valid_sc = False
        if first == second:
            if last != second_last:
                valid_sc = False
            
        if valid_sc:
            filter_scs.append(sc)
    return filter_scs


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


def draw_simple_cycle(sc):
    """ Draw a simple cycle.
    """
    return


def main():
    return


if __name__ == '__main__':
    main()
