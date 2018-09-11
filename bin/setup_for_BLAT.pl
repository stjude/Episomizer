#!/hpcf/apps/perl/install/5.10.1/bin/perl

#This file is part of Episomizer.

#Author: Ke (Corey) Xu, PhD
#Contact: kxu101@gmail.com


$ref_genome = $ARGV[0];     # /research/rgs01/resgen/prod/tartan/runs/ad_hoc/reference_import-Tm4OgjZi/output/reference/Homo_sapiens/GRCh37-lite/2BIT/GRCh37-lite.2bit
$input = $ARGV[1];          # CNA_region_refined.bed
$output = $ARGV[2];         # run_BLAT.sh
open(OUT, ">$output");

open(IN, $input);
@in = <IN>;
close IN;

$CNA_num = $#in + 1;

for($i=1; $i<=$CNA_num; $i++) {
	print OUT "blat -noHead ".$ref_genome." ../trace/CNA_boundary_softclip_fa/seg_".$i."_L_softclip.fa ../trace/CNA_boundary_softclip_BLAT/seg_".$i."_L_softclip.psl", "\n";
	print OUT "blat -noHead ".$ref_genome." ../trace/CNA_boundary_softclip_fa/seg_".$i."_R_softclip.fa ../trace/CNA_boundary_softclip_BLAT/seg_".$i."_R_softclip.psl", "\n";
}

exit;
