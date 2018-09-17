#!/usr/bin/env python3
"""
Testers for graph generation and simple cycle finder.
"""

import unittest
import util


class TestComposer(unittest.TestCase):
    def setUp(self):
        self.tool = 'composer.py circ'
        self.test_data_dir = './testdata'
        self.reviewed_data_dir = '{}/intmd/reviewed_data'.format(self.test_data_dir)
        self.output_dir = '{}/output'.format(self.test_data_dir)
        self.seg_file_relapse = '{}/Reviewed_segments_for_graph_relapse_rawCNA.bed'.format(self.reviewed_data_dir)
        self.edge_file_relapse = '{}/Reviewed_edges_for_graph_relapse_rawCNA.txt'.format(self.reviewed_data_dir)
        self.cmd_input_relapse = '{} -c {} -l {}'.format(self.tool, self.seg_file_relapse, self.edge_file_relapse)
        self.seg_file_diagnosis = '{}/Reviewed_segments_for_graph_diagnosis_rawCNA.bed'.format(self.reviewed_data_dir)
        self.edge_file_diagnosis = '{}/Reviewed_edges_for_graph_diagnosis_rawCNA.txt'.format(self.reviewed_data_dir)
        self.cmd_input_diagnosis = '{} -c {} -l {}'.format(self.tool, self.seg_file_diagnosis, self.edge_file_diagnosis)

    def test_graph_to_sif(self):
        """ Test networkx graph to sif function.
        """
        out_sif_file = '{}/graph_relapse.sif'.format(self.output_dir)
        cmd = '{} -s {}'.format(self.cmd_input_relapse, out_sif_file)
        util.run_shell_command_call(cmd)

    def test_find_cycles_relapse(self):
        """ Test finding all simple cycles for the relapse sample
        """
        out_cycle_file = '{}/double_minutes_relapse.txt'.format(self.output_dir)
        cmd = '{} -d {}'.format(self.cmd_input_relapse, out_cycle_file)
        util.run_shell_command_call(cmd)

    def test_find_cycles_diagnosis(self):
        """ Test finding all simple cycles for the relapse sample
        """
        out_cycle_file = '{}/double_minutes_diagnosis.txt'.format(self.output_dir)
        cmd = '{} -d {}'.format(self.cmd_input_diagnosis, out_cycle_file)
        util.run_shell_command_call(cmd)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
