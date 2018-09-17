#!/usr/bin/env python3
"""
This module contains functions to work with simple cycles on a bidirected graph.
"""

import networkx as nx
import double_minute


def find_simple_cycles(dg):
    """ Find all simple cycles given a networkx graph.
    Args:
        dg (obj): a networkx directed graph
    Returns:
        simple_cycles (list of lists): a list of simple cycles ordered by number of segments.
    """
    simple_cycles = [c for c in nx.simple_cycles(dg) if len(c) > 2]
    #simple_cycles.sort(key=lambda cycle: len(cycle), reverse=True)     # sort by number of segments
    return simple_cycles


def simple_cycle_to_double_minute(graph, simple_cycle):
    """ Convert a simple cycle to a DoubleMintue.
    Args:
        graph (obj): a networkx directed graph that contains the simple cycle
        sc (list): a simple cycle
    Returns:
        double_minute (obj): a DoubleMintue
    """
    dm = double_minute.DoubleMinute()
    if simple_cycle[0][:-1] == simple_cycle[1][:-1]:    # first two nodes form a segment edge
        dm.length += graph[simple_cycle[0][:-1] + 'L'][simple_cycle[1][:-1] + 'R']['Length']
        first_node = simple_cycle.pop(0)
        simple_cycle.append(first_node)
    else:
        dm.length += graph[simple_cycle[0][:-1] + 'L'][simple_cycle[-1][:-1] + 'R']['Length']

    for index, node in enumerate(simple_cycle[:-1]):
        if node[:-1] == simple_cycle[index + 1][:-1]:   # segment
            dm.length += graph[node[:-1] + 'L'][node[:-1] + 'R']['Length']
        else:                                           # non-segment edge
            ord_num1 = node[:-1]
            end1 = node[-1]
            ord_num2 = simple_cycle[index + 1][:-1]
            end2 = simple_cycle[index + 1][-1]
            edge_type = graph[node][simple_cycle[index+1]]['type'][0].lower()
            directed_edge = double_minute.DirectedEdge(ord_num1, end1, ord_num2, end2, edge_type)
            dm.ordered_edges.append(directed_edge)
    return dm


def simple_cycles_to_double_minutes(graph, simple_cycles):
    """ Convert simple cycles to double_minutes, then sort by length.
    Args:
        graph (obj): a networkx directed graph that contains the simple cycle
        simple_cycles (list of lists): a list of simple cycles.
    Returns:
        double_minutes (list): a list of DoubleMinutes.
    """
    double_minutes = []
    for sc in simple_cycles:
        double_minutes.append(simple_cycle_to_double_minute(graph, sc))
    sorted_double_minutes = sorted(double_minutes, key=lambda dm: dm.length, reverse=True)
    return sorted_double_minutes


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
    else:
        total_length += graph[sc[0][:-1] + 'L'][sc[-1][:-1] + 'R']['Length']
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
