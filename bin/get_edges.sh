#!/usr/bin/env bash

unset R_HOME
Rscript --vanilla matrix2edges.R ../input/CNA_region_raw_R.bed ../trace/matrix_softclip.txt ../trace/putative_edges_softclip.txt
Rscript --vanilla matrix2edges.R ../input/CNA_region_raw_R.bed ../trace/matrix_discordant.txt ../trace/putative_edges_discordant.txt
Rscript --vanilla matrix2edges.R ../input/CNA_region_raw_R.bed ../trace/matrix_bridge.txt ../trace/putative_edges_bridge.txt
