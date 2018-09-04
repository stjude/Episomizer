#!/usr/bin/env python3
"""
This module contains functions to work with simple cycles on a bidirected graph.
"""

import networkx as nx


def find_simple_cycles(dg):
    """ Find all simple cycles given a networkx graph.
    Args:
        dg (obj): a networkx directed graph
    Return:
        simple_cycles (list): a list of all simple cycles.
    """
    simple_cycles = [c for c in nx.simple_cycles(dg) if len(c) > 2]
    simple_cycles.sort(key=lambda cycle: len(cycle), reverse=True)
    return simple_cycles


def simple_cycles_to_string(simple_cycles):
    """ Convert simple cycles to a string.
    Args:
        simple_cycles (list of lists): a list of simple cycles.
    Returns:
        None
    """
    to_string = ''
    to_string += 'Number of simple cycles: {}'.format(str(len(simple_cycles)))
    for c in simple_cycles:
        to_string += c
    to_string += '\n'
    return to_string


def simple_cycle_to_string(graph, sc):
    """ Convert a simple cycle to a string.
    Args:
        graph (obj): a networkx directed graph
        sc (list): a simple cycle
    Returns:
        to_string (str): string representation of the simple cycle
    """
    to_string = ''
    total_length = 0
    if sc[0][:-1] == sc[1][:-1]:            # First two nodes form a segment edge
        total_length += graph[sc[0][:-1] + 'L'][sc[1][:-1] + 'R']['Length']
        first_node = sc.pop(0)
        sc.append(first_node)
    in_segment = False
    for index, node in enumerate(sc[:-1]):
        if in_segment:
            to_string += str(node[-1])
        else:
            to_string += str(node)
        if node[:-1] == sc[index+1][:-1]:   # segment edge
            in_segment = True               # next node is in segment
            total_length += graph[node[:-1] + 'L'][node[:-1] + 'R']['Length']
        else:
            to_string += ' -'               # non-segment edge
            to_string += str(graph[node][sc[index+1]]['type'][0].lower())
            to_string += '-> '
            in_segment = False              # next node is not in segment
    if sc[-1][:-1] == sc[-2][:-1]:
        to_string += str(sc[-1][-1])
    else:
        to_string += str(sc[-1])
    to_string += str('\nLength: ' + str(total_length) + '\n')
    return to_string
