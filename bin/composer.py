#!/usr/bin/env python3
"""
Episome composer takes inputs of highly amplified somatic copy number alteration (CNA) segments and
structure variants (SV) associated with the segment boundaries, composes the segments to form simple
cycles as candidates of double minute structures.
"""

import sys
import argparse

import graph
import cycle
import path
import double_minute


def main():
    """ Program entry and argument handler.
    """
    head_description = 'Double minute composer based on CNAs and SVs.'
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=head_description)

    # Create a parent parser with common arguments for every subparser.
    parent_parser = argparse.ArgumentParser(description='double minute composer.', add_help=False)
    parent_parser.add_argument('-v', '--verbose', help='enable verbose mode', action='store_true')
    subparsers = parser.add_subparsers(title='Subcommands', help="Subcommands", dest='subparser_name')

    # Create a subparser for composing double minutes.
    subparser_circ = subparsers.add_parser('circ', help='circular double minute composer', parents=[parent_parser])
    circ_req = subparser_circ.add_argument_group('input arguments')
    circ_req.add_argument('-c', '--cna-segment', metavar='FILE', required=True,
                          help='input bed file containing somatic copy number alteration segments')
    circ_req.add_argument('-l', '--linked-sv', metavar='FILE', required=True,
                          help='input tab-delimited text file containing linked structure variant boundaries')

    circ_sif = subparser_circ.add_argument_group('arguments for creating a sif file for graph displaying')
    circ_sif.add_argument('-s', '--sif', metavar='FILE', help='output sif file')

    circ_dm = subparser_circ.add_argument_group('arguments for generating circular double minutes')
    circ_dm.add_argument('-d', '--circ-dm', metavar='FILE', help='output circular double minute file')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    try:
        args = parser.parse_args()
    except:
        subparser_circ.print_help()
        sys.exit(1)

    circ_handler(args.cna_segment, args.linked_sv, out_sif_file=args.sif, out_dm_file=args.circ_dm)


def circ_handler(cna_segment_file, linked_sv_file, **kwargs):
    """ Build a bidirected graph, find all simple cycles in the graph as candidates of circular double minutes.
    Args:
        Required input arguments:
            cna_segment_file (str): path to a bed file containing somatic copy number alteration segments.
            linked_sv_file (str): path to a tab-delimited text file containing linked structure variant boundaries.
        Optional keyword arguments:
            out_sif_file (str): path to an output sif file (importable in Cytoscape).
            out_dm_file (str): path to an output circular double minute file.
    Returns:
        None
    """
    # Build a directed graph
    dg = graph.build_graph(cna_segment_file, linked_sv_file)

    # Output to a sif file if the argument exists
    if kwargs['out_sif_file']:
        output_graph_to_sif(dg, kwargs['out_sif_file'])
        sys.exit(0)

    # Find double mintues and output to a file if the argument exists
    if kwargs['out_dm_file']:
        find_circular_double_minutes(dg, kwargs['out_dm_file'])
        sys.exit(0)


def output_graph_to_sif(dg, sif_file):
    """ Output the graph to a sif file.
    Args:
        dg (obj): a networkx directed graph object.
        sif_file (str): path to an output sif file.
    Returns:
        None
    """
    print('Outputing the graph to a sif file ...', file=sys.stderr)
    graph.to_sif(dg, sif_file)
    print('Done', file=sys.stderr)


def find_circular_double_minutes(dg, circ_dm_file):
    """ Find all simple cycles.
    Args:
        dg (obj): a networkx directed graph object.
        circ_dm_file (obj): path to an output circular double minute file.
    Returns:
        circ_double_minutes (list): circular double minutes.
    """
    print('Finding circular double minutes ...', file=sys.stderr)
    simple_cycles = cycle.find_simple_cycles(dg)
    filtered_simple_cycles = path.filter_jump_paths(simple_cycles)
    double_minutes = cycle.simple_cycles_to_double_minutes(dg, filtered_simple_cycles)
    deduplicated_simple_cycles = double_minute.rm_reverse_double_minutes(double_minutes)
    with open(circ_dm_file, 'w') as fout:
        fout.write('Number of circular double minutes: ' + str(len(deduplicated_simple_cycles)) + '\n\n')
        for index, dm in enumerate(deduplicated_simple_cycles):
            fout.write('Double minute ' + str(index + 1) + ':\n')
            fout.write(str(dm) + '\n\n')
    print('Done', file=sys.stderr)
    return deduplicated_simple_cycles


if __name__ == '__main__':
    main()