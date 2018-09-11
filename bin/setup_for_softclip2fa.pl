#!/hpcf/apps/perl/install/5.10.1/bin/perl

#This file is part of Episomizer.

#Author: Ke (Corey) Xu, PhD
#Contact: kxu101@gmail.com


$input = $ARGV[0];     # CNA_region_refined.bed
$output = $ARGV[1];    # run_softclip2fa.sh
open(OUT, ">$output");

open(IN, $input);
@in = <IN>;
close IN;

$CNA_num = $#in + 1;

for($i=1; $i<=$CNA_num; $i++) {
	print OUT "perl softclip2fa.pl ../trace/CNA_boundary_reads/seg_".$i."_L ../trace/CNA_boundary_softclip_fa/seg_".$i."_L_softclip.fa", "\n";
	print OUT "perl softclip2fa.pl ../trace/CNA_boundary_reads/seg_".$i."_R ../trace/CNA_boundary_softclip_fa/seg_".$i."_R_softclip.fa", "\n";
}
