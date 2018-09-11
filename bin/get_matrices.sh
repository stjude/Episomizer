perl SV_softclip.pl ../input/CNA_region_raw_R.bed 1000 ../trace/matrix_softclip.txt 
perl SV_discordant.pl ../input/CNA_region_raw_R.bed 800 1000 ../trace/matrix_discordant.txt 
perl SV_bridge.pl ../input/CNA_region_raw_R.bed 800 10000 ../trace/matrix_bridge.txt 
