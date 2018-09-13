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
        self.seg_file_relapse = '{}/inputs/relapse/CNA_region_raw_R.bed'.format(self.test_data_dir)
        self.non_seg_file_relapse = '{}/inputs/relapse/Reviewed_edges_for_graph_relapse_' \
                                    'rawCNA.txt'.format(self.test_data_dir)
        self.cmd_input_relapse = '{} -c {} -l {}'.format(self.tool, self.seg_file_relapse, self.non_seg_file_relapse)
        self.seg_file_diagnosis = '{}/inputs/diagnosis/Reviewed_segments_for_graph_diagnosis.' \
                                  'bed'.format(self.test_data_dir)
        self.non_seg_file_diagnosis = '{}/inputs/diagnosis/Reviewed_edges_for_graph_diagnosis' \
                                      '_rawCNA.txt'.format(self.test_data_dir)
        self.cmd_input_diagnosis = '{} -c {} -l {}'.format(self.tool, self.seg_file_diagnosis,
                                                           self.non_seg_file_diagnosis)

    def test_graph_to_sif(self):
        """ Test networkx graph to sif function.
        """
        out_sif_file = '{}/outputs/relapse/graph.sif'.format(self.test_data_dir)
        cmd = '{} -s {}'.format(self.cmd_input_relapse, out_sif_file)
        util.run_shell_command_call(cmd)

    def test_find_cycles_relapse(self):
        """ Test finding all simple cycles for the relapse sample
        """
        out_cycle_file = '{}/outputs/relapse/double_minutes.txt'.format(self.test_data_dir)
        cmd = '{} -d {}'.format(self.cmd_input_relapse, out_cycle_file)
        util.run_shell_command_call(cmd)

    def test_find_cycles_diagnosis(self):
        """ Test finding all simple cycles for the relapse sample
        """
        out_cycle_file = '{}/outputs/diagnosis/double_minutes.txt'.format(self.test_data_dir)
        cmd = '{} -d {}'.format(self.cmd_input_diagnosis, out_cycle_file)
        util.run_shell_command_call(cmd)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
