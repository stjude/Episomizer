#!/usr/bin/env python
"""
Python version: 2.7.13
Note: this is written to be compatible with python3. But networkx draw does not support
python3 very well. Suggest running in python2.

Author: Liang Ding
Date: 8/18/2017

Circular DNA detector.
"""

import graph
import cycle_v2 as cycle


def main():
    """ Program gate and argument handler.
    """
    circRNA()
    return


def circRNA():
    """ Driver function to detect circular DNA.
        Returns:
            None
    """
    graph_text = '../inputs/softclip_only_S_D.txt'
    dg = graph.build_graph(graph_text)
    simple_cycles = cycle.find_simple_cycles(dg)
    cycle.filter_jump_cycle(simple_cycles)
    return


if __name__ == '__main__':
    main()
