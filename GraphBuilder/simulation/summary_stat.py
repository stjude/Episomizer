#!/usr/bin/env python3

import os
#import sys


def main():
    """ Program gate and argument handler.
    """
    summary_pearson()
    return


def summary_pearson():
    """ Summary cycle abundance test results for the relapse sample.
    """
    output_path = '../outputs/relapse/max_cycle_abundance_estimate/Pearson/nolog/'
    summary_file = '../outputs/relapse/max_cycle_abundance_estimate/Pearson/summary_nolog.txt'
    fout = open(summary_file, 'w')
    fout.write('cycle_cover\tmax_abundance\trank\tPearson_cc\tcycle_abundance\tp_value\n')
    files = [output_path + 'cycle_abundances_m' + str(n) + '.txt' for n in range(2, 18)]
    for txt in files:
        if txt.find('abundances') != -1:
            max_abundance = int(os.path.basename(txt).split('_')[2][1:-4])
            with open(txt, 'r') as fin:
                fin.readline()
                rank = 0
                while True:
                    line = fin.readline().rstrip()
                    if not line:
                        break
                    rank += 1
                    tokens = line.split('\t')
                    correlation = tokens[0]
                    cycle_cover = tokens[1]
                    cycle_abundance = tokens[2]
                    p_value = tokens[3]
                    #if cycle_cover == '1 3 4 5 6 7 ':
                    if cycle_cover == '2 3 4 6 7 ':
                        fout.write(cycle_cover + '\t')
                        fout.write(str(max_abundance) + '\t')
                        fout.write(str(rank) + '\t')
                        fout.write(correlation + '\t')
                        fout.write(cycle_abundance + '\t')
                        fout.write(p_value + '\n')
                        break
    fout.close()
    return


if __name__ == '__main__':
    main()