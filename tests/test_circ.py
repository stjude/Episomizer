#!/usr/bin/env python3
"""
Testers for graph generation and simple cycle finder.
"""

import unittest
import util


class TestComposer(unittest.TestCase):
    def setUp(self):
        self.tool = 'composer.py circ'
        self.test_data_dir = './testdata/composer'
        self.seg_file = '{}/inputs/relapse/CNA_region_raw_R.bed'.format(self.test_data_dir)
        self.non_seg_file = '{}/inputs/relapse/Reviewed_edges_for_graph_relapse_rawCNA.txt'.format(self.test_data_dir)
        self.cmd_input = '{} -c {} -l {}'.format(self.tool, self.seg_file, self.non_seg_file)

    def test_graph_to_sif(self):
        """ Test networkx graph to sif function.
        """
        out_sif_file = '{}/outputs/relapse/graph.sif'.format(self.test_data_dir)
        cmd = '{} -s {}'.format(self.cmd_input, out_sif_file)
        util.run_shell_command_call(cmd)

    def test_find_cycles(self):
        """ Test finding all simple cycles.
        """
        out_cycle_file = '{}/outputs/relapse/double_minutes.txt'.format(self.test_data_dir)
        cmd = '{} -d {}'.format(self.cmd_input, out_cycle_file)
        util.run_shell_command_call(cmd)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
