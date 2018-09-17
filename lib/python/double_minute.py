#!/usr/bin/env python3
"""
Classes related to double minute.
"""

import pybedtools


class Segment(object):
    """ Class for a highly amplified genomic region.
    Attributes:
        chromosome (str): chromosome, e.g., chr7
        left_boundary (int): 5' segment boundary
        right_boundary (int): 3' segment boundary
        ordinal_number (int): ordinal number
    """
    def __init__(self, chromosome=None, left_boundary=None, right_boundary=None, ord_num=None):
        self.chromosome = chromosome
        self.left_boundary = left_boundary
        self.right_boundary = right_boundary
        self.ordinal_number = ord_num


class Segments(object):
    """ Class for a list of highly amplified genomic regions.
    Attributes:
        segments (list): Segment list
    """
    def __init__(self):
        self.segments = []

    def read_from_bed_file(self, cna_segment_file):
        """ Read regions from a bed file and build a list of Segments.
        Args:
            cna_segment_file (str): a bed file containing somatic copy number alteration segments
        """
        raw_segments = pybedtools.BedTool(cna_segment_file)
        for segment in raw_segments:
            chromosome = segment[0]
            left_boundary = int(segment[1])
            right_boundary = int(segment[2])
            ordinal_number = segment[3]
            self.segments.append(Segment(chromosome, left_boundary, right_boundary, ordinal_number))


class DirectedEdge(object):
    """ Class for a directed edge that connects two segment boundaries.
    Attributes:
        segment_ord_num1 (int): ordinal number of 5' segment
        segment_end1 (L or R): left or right end of the first segment
        segment_ord_num2 (int): ordinal number of 3' segment
        segment_end2 (L or R): left or right end of the second segment
        edge_type (str): edge type based on supporting evidence
    """
    def __init__(self, ord_num1=None, end1=None, ord_num2=None, end2=None, edge_type=None):
        self.segment_ord_num1 = ord_num1
        self.segment_end1 = end1
        self.segment_ord_num2 = ord_num2
        self.segment_end2 = end2
        self.edge_type = edge_type

    def __str__(self):
        left_node = '{}{}'.format(self.segment_ord_num1, self.segment_end1)
        right_node = '{}{}'.format(self.segment_ord_num2, self.segment_end2)
        return '{0: ^5}--{1}-->{2: ^5}'.format(left_node, self.edge_type, right_node)


class DoubleMinute(object):
    """ Class for a double minute (circular or linear)
    Attributes:
        length (int): length of the double minute
        ordered_edges (list of DirectedEdges): ordered DirectedEdges forming the double minute
    """
    def __init__(self, length=None, ordered_edges=None):
        if length is None:
            self.length = 0
        else:
            self.length = length

        if ordered_edges is None:
            self.ordered_edges = []
        else:
            self.ordered_edges = ordered_edges

    def __str__(self):
        temp_lst = []
        for index, edge in enumerate(self.ordered_edges):
            if (index+1) % 8 == 0:
                temp_lst.append('\n')
            else:
                temp_lst.append(str(edge))
        edge_str = ''.join(temp_lst)
        return 'Length: {}\nNumber of segments: {}\n{}\n'.format(self.length, len(self.ordered_edges), edge_str)


class CircularDoubleMinute(DoubleMinute):
    """ Class for a circular double minute.
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return


# This is a temporary implementation. path.rm_reverse_paths() should be rewritten and used to replace this one.
def rm_reverse_double_minutes(sorted_double_minutes):
    """ Remove duplicated double mintues with reverse direction.
    Args:
        simple_paths (list): a list of double minutes sorted by length
    Returns:
        List: left paths
    """
    left_double_minutes = []
    for i in range(0, len(sorted_double_minutes)):
        if i % 2 == 1:
            left_double_minutes.append(sorted_double_minutes[i])
    return left_double_minutes
