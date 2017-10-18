#!/usr/bin/env python3
"""
Python version: 3.6

Author: Liang Ding
Date: 10/17/2017

Tester for circDNA.py circ.
"""

import os
import unittest
import subprocess


class TestCircDNA(unittest.TestCase):
    def setUp(self):
        os.chdir('../src/')
        self.seg_file = '../inputs/relapse/edges_for_graph_S_segments.txt'
        self.non_seg_file = '../inputs/relapse/edges_for_graph_S_full.txt'
        self.seg_attr_file = '../inputs/relapse/noCREST_copygain_LR3_details.txt'
        self.cmd_input = './circDNA.py circ -s ' + self.seg_file + ' -n ' + self.non_seg_file\
                         + ' -a ' + self.seg_attr_file

    def test_graph_to_sif(self):
        """ Test networkx graph to sif function.
        """
        out_sif_file = '../outputs/relapse/graph.sif'
        cmd = self.cmd_input + ' -sf ' + out_sif_file
        subprocess.check_call(cmd, shell=True)
        return

    def test_find_cycles(self):
        """ Test finding all simple cycles.
        """
        out_cycle_file = '../outputs/relapse/cycle.txt'
        cmd = self.cmd_input + ' -cy ' + out_cycle_file
        subprocess.check_call(cmd, shell=True)
        return

    def test_find_cycle_covers(self):
        """ Test finding cycle covers.
        """
        out_cycle_file = '../outputs/relapse/cycle.txt'
        out_cycle_cover_file = '../outputs/relapse/cycle_cover.txt'
        cmd = self.cmd_input + ' -cy ' + out_cycle_file + ' -cc ' + out_cycle_cover_file
        subprocess.check_call(cmd, shell=True)
        return

    def test_estimate_abundance_pearsonr(self):
        """ Test estimating cycle/segment abundance using pearsonr cc and log ratio
        """
        out_cycle_file = '../outputs/relapse/cycle.txt'
        out_cycle_cover_file = '../outputs/relapse/cycle_cover.txt'
        max_abundance = 2
        df = 'pearsonr'
        out_cycle_abundance_file = '../outputs/relapse/cycle_abundance_' + df + '.txt'
        cmd = self.cmd_input + ' -cy ' + out_cycle_file + ' -cc ' + out_cycle_cover_file \
              + ' -m ' + str(max_abundance) + ' -df ' + df + ' -lg ' \
              + ' -ca ' + out_cycle_abundance_file
        subprocess.check_call(cmd, shell=True)
        return

    def test_estimate_abundance_euclidean(self):
        """ Test estimating cycle/segment abundance using euclidean distance, ratio (without log),
            and zscore to normalize.
        """
        out_cycle_file = '../outputs/relapse/cycle.txt'
        out_cycle_cover_file = '../outputs/relapse/cycle_cover.txt'
        max_abundance = 2
        df = 'euclidean'
        nf = 'zscore'
        out_cycle_abundance_file = '../outputs/relapse/cycle_abundance_' + df + '.txt'
        cmd = self.cmd_input + ' -cy ' + out_cycle_file + ' -cc ' + out_cycle_cover_file \
              + ' -m ' + str(max_abundance) + ' -df ' + df + ' -nf ' + nf \
              + ' -ca ' + out_cycle_abundance_file
        subprocess.check_call(cmd, shell=True)
        return

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
