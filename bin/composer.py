#!/usr/bin/env python3
"""
Episome composer.
"""

import sys
import argparse

import graph
import cycle
import path


def main():
    """ Program entry and argument handler.
    """
    head_description = 'Circular and linear episome detector from segments.'
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=head_description)

    # Create a parent parser with common arguments for every subparser
    parent_parser = argparse.ArgumentParser(description='Tools for a tartan run.', add_help=False)
    parent_parser.add_argument('-v', '--verbose', help='Enable verbose mode.', action='store_true')
    parent_parser.add_argument('-d', '--debug', help='Enable debug mode.', action='store_true')
    parent_parser.add_argument('--dry-run', help='Enable dry-run mode.', action='store_true')

    subparsers = parser.add_subparsers(title='Subcommands', help='Valid subcommands.', dest='subparser_name')
    # Create a subparser for finding circular episomes
    subparser_circ = subparsers.add_parser('circ', help='Finding circular episomes.', parents=[parent_parser])

    circ_req = subparser_circ.add_argument_group('Input arguments')
    circ_req.add_argument('-s', metavar='FILE', help='Input file with segment edges.')
    circ_req.add_argument('-n', metavar='FILE', help='Input file with non-segment edges.')
    circ_req.add_argument('-a', metavar='FILE', help='Input file with segment attributes.')

    circ_sif = subparser_circ.add_argument_group('Arguments for creating sif file')
    circ_sif.add_argument('-sf', metavar='FILE', help='Output sif file.')

    circ_cycle = subparser_circ.add_argument_group('Arguments for generating cycles')
    circ_cycle.add_argument('-cy', metavar='FILE', help='Output cycle file.')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if len(sys.argv) == 2:
        if args.subparser_name == 'circ':
            subparser_circ.print_help()
            sys.exit(0)

    circ_handler(args.s, args.n, args.a, out_sif_file=args.sf, out_cycle_file=args.cy)


def circ_handler(segment_file, non_segment_file, segment_attribute_file, **kwargs):
    """ Has the functions to build a bidirected graph, find all episome(cycles),
        find all cycle covers, filter false positive cycle covers and estimate cycle abundance.
    Args:
        Required input arguments:
            segment_file (str): path to a file containing segment edges
            non_segment_file (str): path to a file containing non-segment edges
            segment_attribute_file (str): path to a file containing segment attributes
        Optional keyword arguments:
            out_sif_file (str): path to an output sif file (importable in Cytoscape)
            out_cycle_file (str): path to an output file of cycles
    Returns:
            None
    """
    # Build a directed graph
    dg = graph.build_graph(non_segment_file, segment_file, segment_attribute_file=segment_attribute_file)
    if kwargs['out_sif_file']:
        graph_to_sif(dg, kwargs['out_sif_file'])
        sys.exit(0)

    if kwargs['out_cycle_file']:
        find_cycles(dg, kwargs['out_cycle_file'])
        sys.exit(0)


def graph_to_sif(dg, out_sif_file):
    """ Save graph to a sif file.
    Args:
        db (obj): a networkx graph
        out_sif_file (str): path to an output sif file.
    Returns:
        None
    """
    print('Saving graph to sif file ...', file=sys.stderr)
    graph.to_sif(dg, out_sif_file)
    print('Done', file=sys.stderr)


def find_cycles(dg, out_cycle_file):
    """ Find all simple cycles.
    Args:
        dg (obj): a networkx directed graph object
        out_cycle_file (obj): path to an output cycle file
    Returns:
        left_scs (list): list of simple cycles
    """
    print('Finding all cycles ...', file=sys.stderr)
    out_cycle_file = out_cycle_file
    simple_cycles = cycle.find_simple_cycles(dg)
    filtered_scs = path.filter_jump_paths(simple_cycles)
    left_scs = path.rm_reverse_paths(filtered_scs)
    with open(out_cycle_file, 'w') as fout:
        fout.write('Number of cycles: ' + str(len(left_scs)) + '\n')
        for index, sc in enumerate(left_scs):
            fout.write('Cycle ' + str(index + 1) + '\n')
            fout.write(cycle.simple_cycle_to_string(dg, sc) + '\n')
    print('Done', file=sys.stderr)
    return left_scs


if __name__ == '__main__':
    main()

