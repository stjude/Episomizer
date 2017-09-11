$output = "BLAT.sh";
open(OUT, ">$output");

for($i=1; $i<=30; $i++) {
	print OUT "blat -noHead /nfs_exports/genomes/1/Homo_sapiens/Hg19/2BIT/hg19.2bit copygainLR3_boundry_50bp_softclip_fa/seg_".$i."_L_sofclip.fa copygainLR3_boundry_50bp_softclip_BLAT/seg_".$i."_L_sofclip.psl", "\n";
	print OUT "blat -noHead /nfs_exports/genomes/1/Homo_sapiens/Hg19/2BIT/hg19.2bit copygainLR3_boundry_50bp_softclip_fa/seg_".$i."_R_sofclip.fa copygainLR3_boundry_50bp_softclip_BLAT/seg_".$i."_R_sofclip.psl", "\n";
}




