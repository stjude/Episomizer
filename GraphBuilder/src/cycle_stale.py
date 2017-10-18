#!/usr/bin/env python
"""
Python version: 2.7.13
Author: Liang Ding
Date: 8/9/2017

Find simple cycles for a undirected graph.
Different with version 2, this version uses one vertices to represent a segment.
"""

import os
import networkx as nx


def main():
    graph_text = './softclip_only_S.txt'
    simple_cycles = find_simple_cycles(graph_text)
    route_text = './softclip_only_S_D.txt'
    routing(route_text, simple_cycles)
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
            edge_lst.append(tuple([ int(v) for v in line.split('\t')]))
    
    # Create networkx graph object
    dg = nx.DiGraph()
    dg.add_nodes_from(range(1, num_vertices))
    for e in edge_lst:
        dg.add_edge(e[0], e[1])
        dg.add_edge(e[1], e[0])
    
    print('Vertices:')    
    print(dg.nodes())
    print()
    print('Edges:')
    print(dg.edges())
    print()
    
    # Draw directed graph
    #nx.draw(G)
    #plt.savefig('dg.png')
    
    # Compute simple cycles
    print('Simple Cycles:')
    simple_cycles = [c for c in nx.simple_cycles(dg) if len(c) > 2]
    simple_cycles.sort(key=lambda cycle: len(cycle), reverse=True)
    for c in simple_cycles:
        print(c)
    print()
    return simple_cycles


def routing(route_text, simple_cycles):
    """ Routing through each candidate simple cycle and filter those that do not form a circular RNA.
        Args:
            route_text (str): a file with routes
            simple_cycles (list): a list of candidate simple cycles 
        Return:
            List of cycles with routes
    """
    route_dic = dict()
    with open(route_text, 'r') as fin:
        while True:
            line = fin.readline().rstrip()
            if not line:
                break
            tokens = line.split('\t')
            int_node1 = int(tokens[0][:-1])
            int_node2 = int(tokens[1][:-1])
            if (int_node1, int_node2) not in route_dic:
                route_dic[(int_node1, int_node2)] = [(tokens[0], tokens[1])]
            else:
                route_dic[(int_node1, int_node2)].append((tokens[0], tokens[1]))
            if (int_node2, int_node1) not in route_dic:
                route_dic[(int_node2, int_node1)] = [(tokens[1], tokens[0])]
            else:
                route_dic[(int_node2, int_node1)].append((tokens[1], tokens[0]))
    print(route_dic)
    print()
    
    # Routing
    for sc in simple_cycles:
        route_lst = []
        int_node1 = sc[0]
        int_node2 = sc[1]
        stack = []
        for edge in route_dic[(int_node1, int_node2)]:
            stack.append(((0, 1), edge))
        print(stack)
        route_pos = 0   # 0 is the index of the first node
        cur_route = []
        while len(stack) > 0:
            super_edge = stack.pop()
            route_pos += 1
            
            node2 = super_edge[1][1]
            
            if route_pos == len(sc)-1:  # route is at the last node of simple cycle
                route_lst.append(cur_route)
        break
    return


if __name__ == '__main__':
    main()