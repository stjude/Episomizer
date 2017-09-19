#!/usr/bin/env python3
"""
Python version: 3.6
Author: Liang Ding
Date: 8/9/2017

Find simple cycles for a undirected graph.
Different with version 1, this version uses two vertices to represent a segment.
"""

import networkx as nx
import itertools


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
    total_length = 0
    if sp[0][:-1] == sp[1][:-1]:    # First two nodes form a segment edge
        first_node = sp.pop(0)
        sp.append(first_node)
    in_segment = False
    for index, node in enumerate(sp[:-1]):
        if in_segment:
            print(node[-1], end='')
        else:
            print(node, end='')
        if node[:-1] == sp[index+1][:-1]:   # segment edge
            in_segment = True       # next node is in segment
            total_length += graph[node[:-1] + 'L'][node[:-1] + 'R']['Length']
        else:
            print(' -', end='')     # non-segment edge
            print(graph[node][sp[index+1]]['type'][0].lower(), end='')
            print('-> ', end='')
            in_segment = False      # next node is not in segment
    if sp[-1][:-1] == sp[-2][:-1]:
        print(sp[-1][-1])
    else:
        print(sp[-1])
    print('Length: ' + str(total_length) + '\n')
    return


def find_cycle_covers(graph, cycles):
    """ Given all simple cycles, get a set of cycles that covers all segments.
    Args:
        graph (obj): a networkx directed graph object
        cycles (list): all simple cycles.
    """
    num_nodes = nx.number_of_nodes(graph)
    #graph_node_set = set(graph.nodes())
    covers = []
    for i in range(1, len(cycles) + 1):
        for cb in itertools.combinations(cycles, i):
            node_set = set()
            for cycle in cb:
                for node in cycle:
                    node_set.add(node)
            #if len(node_set) == 58:
            #    print(cb)
            #    print(graph_node_set - node_set)
            if len(node_set) == num_nodes:
                covers.append(cb)
    return covers


def print_cycle_cover(covers, sc_dic):
    """ Print a cycle cover.
    Args:
        covers (str): cycle covers.
        sc_dic (dict): dictionary that maps simple cycle index number to simple cycle.
    """
    for index, co in enumerate(covers):
        print('Cover ' + str(index+1) + ': ', end='')
        for cycle in co:
            print(sc_dic[str(cycle)], end=' ')
        print()
    return


def main():
    return


if __name__ == '__main__':
    main()
