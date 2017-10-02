#!/usr/bin/env bash

prog_dir='/home/lding/Dropbox/Git/circDNA/GraphBuilder'

$prog_dir/src/circDNA.py circ -s $prog_dir/inputs/diagnosis/case2/edges_for_graph_E_segments.txt \
     -n $prog_dir/inputs/diagnosis/case2/edges_for_graph_E.txt \
     -a $prog_dir/inputs/diagnosis/case2/E_copygain_LR3_details.txt \
     -f $prog_dir/outputs/diagnosis/case2/graph.sif \
     -c $prog_dir/outputs/diagnosis/case2/cycles.txt