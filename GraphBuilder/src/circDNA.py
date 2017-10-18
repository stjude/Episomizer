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
import cycle
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

    circ_req = subparser_circ.add_argument_group('Input arguments')
    circ_req.add_argument('-s', metavar='FILE', help='Input file with segment edges.')
    circ_req.add_argument('-n', metavar='FILE', help='Input file with non-segment edges.')
    circ_req.add_argument('-a', metavar='FILE', help='Input file with segment attributes.')

    circ_sif = subparser_circ.add_argument_group('Arguments for creating sif file')
    circ_sif.add_argument('-sf', metavar='FILE', help='Output sif file.')

    circ_cycle = subparser_circ.add_argument_group('Arguments for generating cycles')
    circ_cycle.add_argument('-cy', metavar='FILE', help='Output cycle file.')

    circ_cover = subparser_circ.add_argument_group('Arguments for generating cycle covers')
    circ_cover.add_argument('-cc', metavar='FILE', help='Output cycle cover file.')

    circ_abun = subparser_circ.add_argument_group('Arguments for estimating cycle abundance')
    circ_abun.add_argument('-m', metavar='INT', type=int, help='Maximum cycle abundance.')
    circ_abun.add_argument('-ln', help='List available normalization methods.', action='store_true')
    circ_abun.add_argument('-nf', metavar='STR', help='Normalization function name.')
    circ_abun.add_argument('-ld', help='List available distance functions.', action='store_true')
    circ_abun.add_argument('-df', metavar='STR', help='Distance function name.')
    circ_abun.add_argument('-lg', help='Use log ratio. Otherwise just ratio.', action='store_true')
    circ_abun.add_argument('-ca', metavar='FILE', help='Output cycle abundance file.')

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

    if args.m:
        if args.m < 1 or args.m > 20:
            sys.exit('Error - max cycle abundance cannot be less than 1 or greater than 20.')

    avail_dis_funcs = ['pearsonr', 'euclidean']
    normalize_methods = ['zscore']

    if args.ln:
        print('Available normalization functions:')
        for nm in normalize_methods:
            print(nm)
        sys.exit(0)

    if args.ld:
        print('Available distance functions:')
        for df in avail_dis_funcs:
            print(df)
        sys.exit(0)

    if args.df:
        if args.df not in avail_dis_funcs:
            print('Error - invalid distance function: ' + args.df, file=sys.stderr)
            sys.exit(1)

    if args.nf:
        if args.nf not in normalize_methods:
            print('Error - invalid normalization function: ' + args.nf, file=sys.stderr)
            sys.exit(1)

    circ_handler(args.s, args.n, args.a,
            out_sif_file=args.sf,
            out_cycle_file=args.cy,
            out_cycle_cover_file=args.cc,
            max_abundance=args.m,
            df=args.df,
            nf=args.nf,
            lg=args.lg,
            out_cycle_abundance_file=args.ca)

    #linearDNA()
    return


def print_distance_functions(avail_dis_funcs):
    """ Print available distance functions.
    """
    for df in avail_dis_funcs:
        print(df)
    return


def print_normalize_methods(normalize_methods):
    """ Print available normalization methods.
    """
    for nm in normalize_methods:
        print(nm)
    return


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
            out_cycle_cover_file (str): path to an output file of cycle coves
            max_abundance (str): maximum cycle abundance
            df (str): distance function used to estimate cycle/segment abundance
            nf (str): normalization functino used to estimate cycle/segment abundance
            lg (bool): use log ratio or just ratio.
            out_cycle_abundance_file (str): path to an output file of cycle abundance files
        Returns:
            None
    """
    # Build a directed graph
    dg = graph.build_graph(non_segment_file, segment_file, segment_attribute_file=segment_attribute_file)
    if kwargs['out_sif_file']:
        graph_to_sif(dg, kwargs['out_sif_file'])
        sys.exit(0)

    if kwargs['out_cycle_abundance_file']:
        if not kwargs['out_cycle_cover_file']:
            print('Error - out_cycle_cover_file must be provided.', file=sys.stderr)
            sys.exit(1)
        if not kwargs['out_cycle_file']:
            print('Error - out_cycle_file must be provided.', file=sys.stderr)
            sys.exit(1)
        if not kwargs['max_abundance']:
            print('Error - max_abundance must be provided.', file=sys.stderr)
            sys.exit(1)
        left_scs = find_cycles(dg, kwargs['out_cycle_file'])
        cycle_covers = find_cycle_covers(dg, left_scs, kwargs['out_cycle_cover_file'])
        estimate_cycle_abundance(left_scs, cycle_covers, kwargs['max_abundance'],
                                 segment_attribute_file, kwargs['df'],
                                 kwargs['out_cycle_abundance_file'],
                                 norm_func_name=kwargs['nf'], log_ratio=kwargs['lg'])
        sys.exit(0)

    if kwargs['out_cycle_cover_file']:
        if not kwargs['out_cycle_file']:
            print('Error - out_cycle_file must be provided.', file=sys.stderr)
            sys.exit(1)
        left_scs = find_cycles(dg, kwargs['out_cycle_file'])
        find_cycle_covers(dg, left_scs, kwargs['out_cycle_cover_file'])
        sys.exit(0)

    if kwargs['out_cycle_file']:
        find_cycles(dg, kwargs['out_cycle_file'])
        sys.exit(0)
    return


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
    return


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


def find_cycle_covers(dg, left_scs, out_cycle_cover_file):
    """ Find all cycle covers.
    Args:
        dg (obj): networkx directed graph
        left_scs (list): list of simple cycles
        out_cycle_cover_file (str): path to an output cycle cover file
    Returns:
        covers (list): list of cycle covers.
    """
    print('Finding all cycle covers ...', file=sys.stderr)
    sc_dic = dict()
    for index, sc in enumerate(left_scs):
        sc_dic[str(sc)] = index + 1
    covers = cycle.find_cycle_covers(dg, left_scs)
    with open(out_cycle_cover_file, 'w') as fout:
        fout.write(cycle.cycle_covers_to_string(covers, sc_dic))
    print('Done', file=sys.stderr)
    return covers


def estimate_cycle_abundance(left_scs, cycle_covers, max_abundance, segment_attribute_file, df_name,
                             out_cycle_abundance_file, **kwargs):
    """ Estimate cycle abundance and segment abundance.
    Required Args:
        left_scs (list): a list of cycles
        cycle_covers (list): a list of cycle covers
        max_abundance (int): maximum cycle abundance
        segment_attribute_file (str): path to an input segment attribute file
        df_name (str): distance function name
        out_cycle_abundance_file (str): path to an output cycle abundance file
    Optional Keyword Arguments:
        norm_func_name (str): normalization function name.
        log_ratio (bool): use LogRatio. Otherwise, just use ratio.
    Returns:
        None
    """
    sc_dic = dict()
    for index, sc in enumerate(left_scs):
        sc_dic[str(sc)] = index + 1
    print('Calculating the best cycle abundance ...', file=sys.stderr)
    best_cycle_abundances = cycle.best_cover(cycle_covers, max_abundance, segment_attribute_file,
                                             sc_dic, df_name, **kwargs)

    with open(out_cycle_abundance_file, 'w') as fout:
        if df_name == 'pearsonr':
            fout.write('pearsonr_cc\tcycle_cover\tcycle_abundance\tP_value\n')
            for ca in best_cycle_abundances:
                fout.write(str(ca[0]) + '\t')
                fout.write(str(ca[1]) + '\t')
                fout.write(str(ca[2]) + '\t')
                fout.write(str(ca[3]) + '\n')
        else:
            fout.write('Distance\tcycle_cover\tcycle_abundance\n')
            for ca in best_cycle_abundances:
                fout.write(str(0 - ca[0]) + '\t')
                fout.write(str(ca[1]) + '\t')
                fout.write(str(ca[2]) + '\n')
    print('Done', file=sys.stderr)
    return


def linear_handler():
    """ Driver function to find linear DNAs.
    """
    non_segment_file = '../inputs/edges_for_graph_E_linear.txt'
    segment_file = '../inputs/edges_for_graph_E_segments_linear.txt'
    dg = graph.build_graph(non_segment_file, segment_file)
    sif_file = '../outputs/edges_for_graph_E.sif'
    graph.to_sif(dg, sif_file)
    find_linear_DNA(dg)
    return


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
