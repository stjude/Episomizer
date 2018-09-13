#!/usr/bin/env perl

# This file is part of Episomizer.
# Author: Ke (Corey) Xu, PhD and Liang (Adam) Ding, PhD
# Contact: kxu101@gmail.com

use strict;
use warnings;

if (@ARGV == 0) {
    print STDERR "Usage:\n";
    print STDERR "  create_softclip2fa_cmd.pl INPUT_CNA_BED OUTPUT_DIR\n";
    exit 1;
}

my $input_cna_bed = $ARGV[0];	# Path to an input CNA segment bed file
my $output_dir = $ARGV[1];      # Path ot an output directory
my $softclip_fa_dir = $output_dir."/CNA_boundary_softclip_fa";
if (! -d $softclip_fa_dir) {
    mkdir $softclip_fa_dir;
}

open(OUT, ">$output_dir/run_softclip2fa.sh");
open(IN, $input_cna_bed);
my @in = <IN>;
close IN;

my $CNA_num = $#in + 1;
for(my $i=1; $i<=$CNA_num; $i++) {
	print OUT "softclip2fa.pl ".$output_dir."/CNA_boundary_reads/seg_".$i."_L "
        .$softclip_fa_dir."/seg_".$i."_L_softclip.fa", "\n";
	print OUT "softclip2fa.pl ".$output_dir."/CNA_boundary_reads/seg_".$i."_R "
        .$softclip_fa_dir."/seg_".$i."_R_softclip.fa", "\n";
}
close OUT1;
print STDERR "softclip2fa command file was created successfully: ".$output_dir."/run_softclip2fa.sh\n";
exit;
