#!/usr/bin/env python
"""
Python version: 2.7.13
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


def draw_simple_path(graph, sp):
    """ Draw a simple path or cycle.
    Args:
        graph (obj): a networkx graph
        sp (list): a simple path
    Returns:
        None
    """
    for node in sp[:-1]:
        print(node, end='')
        print('--->')
    print(sp[-1])
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


def main():
    return


if __name__ == '__main__':
    main()
