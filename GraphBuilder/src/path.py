#!/usr/bin/env python3
"""
Python version: 3.6
Author: Liang Ding
Date: 8/18/2017

This module finds simple paths.
"""

import networkx as nx


def find_simple_paths(graph, s_node, t_node):
    """ Find all simple paths in the graph G from source to target.
    Args:
        graph (obj): networkx graph object
        s_node (node): Starting node for path
        t_node (node): Ending node for path
    Returns:
        List: a list of all simple paths
    """
    return list(nx.all_simple_paths(graph, source=s_node, target=t_node))


def print_simple_path(graph, sp):
    """ Print a simple path or cycle.
    Args:
        graph (obj): a networkx graph
        sp (list): a simple path
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
            print(graph[node][sp[index+1]]['type'][0], end='')
            print('-> ', end='')
            in_segment = False      # next node is not in segment
    if sp[-1][:-1] == sp[-2][:-1]:
        print(sp[-1][-1] + '\n')
    else:
        print(sp[-1] + '\n')
    return


def filter_jump_paths(simple_paths):
    """ Filter jump simple path or simple cycle(as a special case of simple path).
        Args:
            simple_paths (list): a list of simple paths, where each path is a list.
        Return:
            List: a list of filtered simple paths.
    """
    filter_scs = []
    for sc in simple_paths:
        valid_sc = True
        for i in range(0, len(sc) - 2):
            node1 = sc[i][:-1]
            node2 = sc[i + 1][:-1]
            node3 = sc[i + 2][:-1]
            # Filter jump in the middle of a simple cycle
            # There should not be 3 consecutive different nodes
            if node1 != node2 and node2 != node3:
                valid_sc = False
                break

        # Filter jump at the end of a sc
        first = sc[0][:-1]
        second = sc[1][:-1]
        last = sc[-1][:-1]
        second_last = sc[-2][:-1]
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


def rm_reverse_paths(simple_paths):
    """ Remove reverse cycles/paths from a list of cycles/paths.
        Note: Assume a path and its reverse one are next to each other in the input list!
    Args:
        simple_paths (list): a list of simple paths
    Returns:
        List: left paths
    """
    left_paths = []
    for i in range(0, len(simple_paths)):
        if i % 2 == 1:
            left_paths.append(simple_paths[i])
    return left_paths


def main():
    return


if __name__ == '__main__':
    main()