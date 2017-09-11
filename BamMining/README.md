# Looking for SV at segment boundaries

### First, get the reads around the boundaries: 
   boundries_for_samtools.pl/run the generated .sh

### Then, search for SV. This procedure include three components:
1) softclip reads (currently done segment by segment, but should be combined as one run. Output is a matrix.)   
   softclip_to_fa.pl/write_sh.pl/run the generated .sh   
   write_sh_for_BLAT.pl/run the generated .sh   
   BLAT_mining.pl/write_sh_for_BLAT_mining.pl/run the generated .sh/cat the output files
   
2) discordant reads (one run. Output is a matrix.)   
   discordant.pl
   
3) bridging discordant reads (one run. Output is a matrix.)   
   discordant_sharedhits.pl
   
### Lastly, convert each of the matrix to an edge file for manual review
   matrix2edges_S.R
   
   
### After manual review, combine all the reviewed edges together for graph consturction.
   