#!/usr/bin/env python3
"""
Python version: 3.6

Author: Liang Ding
Date: 8/18/2017

Episome detector.
"""

import sys
import argparse
import itertools

import graph
import cycle_v2 as cycle
import path


def main():
    """ Program gate and argument handler.
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
    circ_req = subparser_circ.add_argument_group('required input arguments')
    circ_req.add_argument('-s', '--seg', metavar='segment_file', required=True, help='Input file with segment edges.')
    circ_req.add_argument('-n', '--non-seg', metavar='non_segment_file', required=True, help='Input file with non-segment edges.')
    circ_req.add_argument('-a', '--seg-attr', metavar='segment_attribute_file', required=True, help='Input file with segment attributes.')
    subparser_circ.add_argument('-c', '--out-cycle', metavar='', help='Output cycle file.')
    subparser_circ.add_argument('-e', '--out-cover', metavar='', help='Output cycle cover file.')
    subparser_circ.add_argument('-m', '--max-abun', metavar='', type=int, help='Maximum cycle abundance.')
    subparser_circ.add_argument('-u', '--out-abun', metavar='', help='Output cycle abundance file.')
    subparser_circ.add_argument('-f', '--out-sif', metavar='', help='Output sif file.')

    # Create a subparser for finding linear episomes
    subparser_linear = subparsers.add_parser('linear', help='Finding linear episomes.', parents=[parent_parser])

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if len(sys.argv) == 2:
        if args.subparser_name == 'circ':
            subparser_circ.print_help()
            sys.exit(0)
        elif args.subparser_name == 'linear':
            subparser_linear.print_help()
            sys.exit(0)

    circDNA(args.seg, args.non_seg, args.seg_attr,
            out_cycle_file=args.out_cycle,
            out_cycle_cover_file=args.out_cover,
            max_abundance=args.max_abun,
            out_cycle_abundance_file=args.out_abun,
            out_sif_file=args.out_sif)

    #linearDNA()
    return


def circDNA(segment_file, non_segment_file, segment_attribute_file, **kwargs):
    """ Function to build a bidirected graph; find all episome(cycles); find all cycle covers;
        filter false positive cycle covers and estimate cycle abundance.
    Args:
        Required input arguments:
            segment_file (str): path to a file containing segment edges
            non_segment_file (str): path to a file containing non-segment edges
            segment_attribute_file (str): path to a file containing segment attributes
        Optional keyword arguments:
            out_sif_file (str): path to sif output file (importable in Cytoscape)
            out_cycle_file (str): path to a output file of cycles
            out_cycle_cover_file (str): path to output file of cycle coves
            max_abundance (str): maximum cycle abundance
            out_cycle_abundance_file (str): path to output file of cycle abundance files
        Returns:
            out_cycle_file: a file contains all cycles.
            out_cycle_cover_file: a file contains all cycle covers.
            out_cycle_abundance_file: a file contains best cycle abundances.
            out_sif_file: a sif file of graph.
    """
    # Build a directed graph
    dg = graph.build_graph(non_segment_file, segment_file, segment_attribute_file=segment_attribute_file)
    if kwargs['out_sif_file']:
        print('Saving graph to sif file ...', file=sys.stderr)
        graph.to_sif(dg, kwargs['out_sif_file'])
        print('Done', file=sys.stderr)

    if kwargs['out_cycle_file']:
        print('Finding all cycles ...', file=sys.stderr)
        out_cycle_file = kwargs['out_cycle_file']
        left_scs = find_circ_DNA(dg)
        with open(out_cycle_file, 'w') as fout:
            fout.write('Number of cycles: ' + str(len(left_scs)) + '\n')
            for index, sc in enumerate(left_scs):
                fout.write('Cycle ' + str(index+1) + '\n')
                fout.write(cycle.simple_cycle_to_string(dg, sc) + '\n')
        print('Done', file=sys.stderr)

        if kwargs['out_cycle_cover_file']:
            print('Finding all cycle covers ...', file=sys.stderr)
            out_cycle_cover_file = kwargs['out_cycle_cover_file']
            sc_dic = dict()
            for index, sc in enumerate(left_scs):
                sc_dic[str(sc)] = index + 1
            covers = cycle.find_cycle_covers(dg, left_scs)
            with open(out_cycle_cover_file, 'w') as fout:
                fout.write(cycle.cycle_covers_to_string(covers, sc_dic))
            print('Done', file=sys.stderr)

            if kwargs['max_abundance'] and kwargs['out_cycle_abundance_file']:
                print('Calculating the best cycle abundance ...', file=sys.stderr)
                max_abundance = kwargs['max_abundance']
                out_cycle_abundance_file = kwargs['out_cycle_abundance_file']
                best_cycle_abundances = cycle.best_cover(covers, max_abundance, segment_attribute_file, sc_dic, 'pearsonr')
                with open(out_cycle_abundance_file, 'w') as fout:
                    fout.write('Pearson_cc\tcycle_cover\tcycle_abundance\tP-value\n')
                    for ca in best_cycle_abundances:
                        fout.write(str(ca[0]) + '\t')
                        fout.write(str(ca[1]) + '\t')
                        fout.write(str(ca[2]) + '\t')
                        fout.write(str(ca[3]) + '\n')
                print('Done', file=sys.stderr)
        return


def linearDNA():
    """ Driver function to find linear DNAs.
    """
    non_segment_file = '../inputs/edges_for_graph_E_linear.txt'
    segment_file = '../inputs/edges_for_graph_E_segments_linear.txt'
    dg = graph.build_graph(non_segment_file, segment_file)
    sif_file = '../outputs/edges_for_graph_E.sif'
    graph.to_sif(dg, sif_file)
    find_linear_DNA(dg)
    return


def find_circ_DNA(dg):
    """ Find and print all circular DNAs
    Args:
        dg (obj): a networkx directed graph object
    Returns:
        List: a list of circular DNAs
    """
    simple_cycles = cycle.find_simple_cycles(dg)
    filtered_scs = path.filter_jump_paths(simple_cycles)
    left_scs = path.rm_reverse_paths(filtered_scs)
    return left_scs


def find_linear_DNA(dg):
    """ Find and print all linear DNAs
    Args:
        dg (obj): a networkx directed graph object
    Returns:
        List: a list of linear DNAs
    """
    # Find all dangling nodes
    dangling_nodes = graph.find_dangling_nodes(dg)
    print('Dangling nodes: ', end='')
    for node in dangling_nodes:
        print(node + ' ', end='')
    print('')

    # Find all simple paths from a source to a destination
    for n_pair in itertools.combinations(dangling_nodes, 2):
        print('s: ' + n_pair[0] + '\td: ' + n_pair[1])
        simple_paths = path.find_simple_paths(dg, n_pair[0], n_pair[1])
        filtered_sps = path.filter_jump_paths(simple_paths)
        for sp in filtered_sps:
            path.print_simple_path(dg, sp)
    return


if __name__ == '__main__':
    main()
