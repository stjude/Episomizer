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
import math
import heapq
from scipy.stats.stats import pearsonr
#from scipy.spatial.distance import euclidean

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


def simple_cycles_to_string(simple_cycles):
    """ Convert simple cycles to a string.
        Args:
            simple_cycles (list): a list of lists
        Returns:
            None
    """
    to_string = ''
    to_string += 'Number of simple cycles: ' + str(len(simple_cycles))
    for c in simple_cycles:
        to_string += c
    to_string += '\n'
    return to_string


def simple_cycle_to_string(graph, sc):
    """ Convert a simple cycle to a string.
    Args:
        graph (obj): a networkx graph
        sc (list): a simple cycle
    Returns:
        None
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


def cycle_covers_to_string(covers, sc_dic):
    """ Convert cycle covers to a string.
    Args:
        covers (str): cycle covers.
        sc_dic (dict): dictionary that maps simple cycle index number to simple cycle.
    Returns:
        to_string (str): string representation of cycle covers
    """
    to_string = ''
    for index, co in enumerate(covers):
        to_string += 'Cover ' + str(index+1) + ': '
        to_string += cycle_cover_to_string(co, sc_dic)
        to_string += '\n'
    return to_string


def cycle_cover_to_string(cover, sc_dic):
    """ Convert a cycle cover to a string.
    Args:
        cover (str): a cycle cover.
        sc_dic (dict): dictionary that maps simple cycle index number to simple cycle.
    Returns:
        to_string (str): string representation of a cycle cover.
    """
    to_string = ''
    for cycle in cover:
        to_string += str(sc_dic[str(cycle)]) + ' '
    return to_string


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
        segment_abundances = []
        for key in sorted(list(segment_count_dict.keys())):
            segment_abundances.append(segment_count_dict[key])
        yield (product, segment_abundances)


@util.timeit
def best_cover(covers, max_abundance, segment_attribute_file, sc_dic, dis_func_name):
    """ Return the best cycle cover and cycle abundance by calculating the largest
        Pearson correlation coefficient of segment counts and LogRatios for every
        cycle abundance in a cover.
    Args:
        covers (list of lists): a list of cycle covers
        max_abundance (int): maximum number of copies of a cycle.
        segment_attribute_file (str): file with attributes (LogRatio, Length, etc) for segment edges.
        sc_dic (dict): dictionary that maps from a cycle cover to its index in a list of cycle covers.
        dis_func_name (str): distance function name.
    Returns:
        best_cover
        best_product
        best_segment_count_lst
        largest_pearsonr
        best_p_value
    """
    #logratio_lst = []
    ratio_lst = []
    with open(segment_attribute_file, 'r') as fin:
        fin.readline()
        while True:
            line = fin.readline().rstrip()
            if not line:
                break
            #logratio_lst.append(float(line.split('\t')[2]))
            ratio_lst.append(math.pow(2, float(line.split('\t')[2])))

    heap = []
    for cover in covers:    # iterate over all covers
        for (product, segment_abundances) in cycle_abundance(cover, max_abundance):  # iterate over all cycle abundance
            dis_func = eval(dis_func_name)
            (pearson_cc, p_value) = dis_func(ratio_lst, segment_abundances)
            if len(heap) < 100:
                heapq.heappush(heap, (pearson_cc, cycle_cover_to_string(cover, sc_dic), product, p_value))
            else:
                if heap[0][0] < pearson_cc:
                    heapq.heappop(heap)
                    heapq.heappush(heap, (pearson_cc, cycle_cover_to_string(cover, sc_dic), product, p_value))
    sorted_by_pearson_cc = sorted(heap, key=lambda tup: tup[0], reverse=True)
    return sorted_by_pearson_cc


def main():
    return


if __name__ == '__main__':
    main()