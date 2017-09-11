$output = "softclip_to_fa.sh";
open(OUT, ">$output");

for($i=1; $i<=30; $i++) {
	print OUT "perl softclip_to_fa.pl copygainLR3_boundry_50bp_allreads/seg_".$i."_L copygainLR3_boundry_50bp_softclip_fa/seg_".$i."_L_sofclip.fa", "\n";
	print OUT "perl softclip_to_fa.pl copygainLR3_boundry_50bp_allreads/seg_".$i."_R copygainLR3_boundry_50bp_softclip_fa/seg_".$i."_R_sofclip.fa", "\n";
}




