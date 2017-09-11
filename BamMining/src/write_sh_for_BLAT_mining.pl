$output = "BLAT_mining.sh";
open(OUT, ">$output");

for($i=1; $i<=30; $i++) {
	print OUT "perl BLAT_mining.pl copygainLR3_boundry_50bp_softclip_BLAT/seg_".$i."_L_sofclip.psl copygainLR3_boundry_50bp_softclip_matrix/seg_".$i."_L_sofclip", "\n";
	print OUT "perl BLAT_mining.pl copygainLR3_boundry_50bp_softclip_BLAT/seg_".$i."_R_sofclip.psl copygainLR3_boundry_50bp_softclip_matrix/seg_".$i."_R_sofclip", "\n";
}




