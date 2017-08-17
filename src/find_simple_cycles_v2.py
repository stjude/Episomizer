#!/usr/bin/env python
"""
Python version: 3.5.2
Author: Liang Ding
Date: 8/9/2017

Find simple cycles for a undirected graph.
Different with version 1, this version uses two vertices to represent a segment.
"""

import os
import networkx as nx
import copy
import matplotlib.pyplot as plt


def main():
    graph_text = './softclip_only_S_D.txt'
    simple_cycles = find_simple_cycles(graph_text)
    filter_jump_cycle(simple_cycles)
    return


def find_simple_cycles(graph_text):
    """ Read a text file with number of nodes and edges. Create a networkx graph. Find and return
        all simple cycles.
        Args:
            graph_text (str): a text file with the first line number of vertices follows 
                a list of edges with one edge per line.
        Return:
            A networkx graph object.
    """
    # Read graph text file
    edge_lst = []
    with open(graph_text, 'r') as fin:
        num_vertices = int(fin.readline().rstrip())
        while True:
            line = fin.readline().rstrip()
            if not line:
                break
            edge_lst.append(tuple([ v for v in line.split('\t')]))
    
    # Create networkx graph object
    dg = nx.DiGraph()
    # Add two nodes for every segment; add segment edges
    for i in range(0, 30):
        dg.add_node(str(i+1) + 'L')
        dg.add_node(str(i+1) + 'R')
        dg.add_edge(str(i+1) + 'L', str(i+1) + 'R')
        dg.add_edge(str(i+1) + 'R', str(i+1) + 'L')
    # Add non-segment edges
    for e in edge_lst:
        dg.add_edge(e[0], e[1])
        dg.add_edge(e[1], e[0])
    
    #nx.draw(dg)
    #nx.draw_circular(dg)
    #plt.show()

    print('Number of vertices: ' + str(len(dg.nodes())))    
    #print(dg.nodes())
    #print('\n')
    print('Number of edges: ' + str(len(dg.edges())))
    #print(dg.edges())
    #print('\n')
    
    # Draw directed graph
    #nx.draw(G)
    #plt.savefig('dg.png')
    
    # Compute simple cycles
    simple_cycles = [c for c in nx.simple_cycles(dg) if len(c) > 2]
    simple_cycles.sort(key=lambda cycle: len(cycle), reverse=True)
    
    print('Number of simple cycles: ' + str(len(simple_cycles)))
    #for c in simple_cycles:
    #    print(c)
    #print('\n')
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
    
    print('Number of filtered simple cycles: ' + str(len(filter_scs)))
    for c in filter_scs:
        print(c)
    print
    return filter_scs


def draw_sc(sc):
    """ Draw a simple cycle.
    """
    return

if __name__ == '__main__':
    main()
