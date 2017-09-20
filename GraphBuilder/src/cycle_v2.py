#!/usr/bin/env python3
"""
Python version: 3.6
Author: Liang Ding
Date: 8/9/2017

Find simple cycles for a bidirected graph.
Different with version 1, this version uses two vertices to represent a segment.
"""

import networkx as nx
import itertools
from scipy.stats.stats import pearsonr

import util


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


def print_cycle_covers(covers, sc_dic):
    """ Print cycle covers.
    Args:
        covers (str): cycle covers.
        sc_dic (dict): dictionary that maps simple cycle index number to simple cycle.
    """
    for index, co in enumerate(covers):
        print('Cover ' + str(index+1) + ': ', end='')
        print_cycle_cover(co, sc_dic)
    return


def print_cycle_cover(cover, sc_dic):
    """ Print a cycle cover.
    Args:
        covers (str): a cycle cover.
        sc_dic (dict): dictionary that maps simple cycle index number to simple cycle.
    """
    for cycle in cover:
        print(sc_dic[str(cycle)], end=' ')
    print()
    return


def cycle_abundance(cover, max_abundance):
    """ Assume a cycle has a maximum number of copies (max_abundance).
        This function enumerates all Cartesian products of cycle abundance in a cover.
    Args:
        cover (list): a list of cycles that cover all segments.
        max_abundance (int): maximum number of copies of a cycle.
    Returns:
        (product, segment_count_lst) (tuple generator):
            product (tuple): cycle abundance in a cover.
            segment_count_lst (list): segment counts corresponding to the cycle abundance
    """
    num_cycles = len(cover)
    for product in itertools.product(range(1, max_abundance+1), repeat=num_cycles):
        segment_count_dict = dict()
        for index, copy_number in enumerate(product):
            for segment in cover[index]:
                seg_num = int(segment[:-1])
                if seg_num in segment_count_dict:
                    segment_count_dict[int(segment[:-1])] += copy_number
                else:
                    segment_count_dict[int(segment[:-1])] = copy_number
        for key in segment_count_dict:
            segment_count_dict[key] = float(segment_count_dict[key] / 2)
        segment_count_lst = []
        for key in sorted(list(segment_count_dict.keys())):
            segment_count_lst.append(segment_count_dict[key])
        yield (product, segment_count_lst)


@util.timeit
def best_cover_pearsonr(covers, max_abundance, segment_attribute_file):
    """ Return the best cycle cover and cycle abundance by calculating the largest
        Pearson correlation coefficient of segment counts and LogRatios for every
        cycle abundance in a cover.
    Args:
        covers (list of lists): a list of cycle covers
        max_abundance (int): maximum number of copies of a cycle.
        segment_attribute_file (str): file with attributes (LogRatio, Length, etc) for segment edges.
    Returns:
        best_cover
        best_product
        best_segment_count_lst
        largest_pearsonr
        best_p_value
    """
    logratio_lst = []
    with open(segment_attribute_file, 'r') as fin:
        fin.readline()
        while True:
            line = fin.readline().rstrip()
            if not line:
                break
            logratio_lst.append(float(line.split('\t')[2]))

    largest_pearsonr = -1.0
    best_p_value = 0.0
    best_cover = []
    best_product = ()
    best_segment_count_lst = []
    for cover in covers[:1]:    # iterate over all covers
        for (product, segment_count_lst) in cycle_abundance(cover, max_abundance):  # iterate over all cycle abundance
            (pearson_cc, p_value) = pearsonr(logratio_lst, segment_count_lst)
            if pearson_cc > largest_pearsonr:
                largest_pearsonr = pearson_cc
                best_p_value = p_value
                best_cover = cover
                best_product = product
                best_segment_count_lst = segment_count_lst
    return best_cover, best_product, best_segment_count_lst, largest_pearsonr, best_p_value


def main():
    return


if __name__ == '__main__':
    main()
