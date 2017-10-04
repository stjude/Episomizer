#!/usr/bin/env bash

prog_dir='/home/lding/Dropbox/Git/circDNA/GraphBuilder'
case='case3'

$prog_dir/src/circDNA.py circ -s $prog_dir/inputs/diagnosis/${case}/edges_for_graph_E_segments.txt \
     -n $prog_dir/inputs/diagnosis/${case}/edges_for_graph_E.txt \
     -a $prog_dir/inputs/diagnosis/${case}/E_copygain_LR3_details.txt \
     -f $prog_dir/outputs/diagnosis/${case}/graph.sif \
     -c $prog_dir/outputs/diagnosis/${case}/cycles.txt