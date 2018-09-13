#!/usr/bin/env perl

# This file is part of Episomizer.
# Author: Ke (Corey) Xu, PhD and Liang (Adam) Ding
# Contact: kxu101@gmail.com

use strict;
use warnings;

if (@ARGV == 0) {
    print STDERR "Usage:\n";
    print STDERR "  create_blat_cmd.pl REF_GENOME_BIT INPUT_CNA_BED OUTPUT_DIR\n";
    exit 1;
}

my $ref_genome = $ARGV[0];      # Path to reference genome GRCh37-lite.2bit file
my $input_cna_bed = $ARGV[1];   # Path to an input CNA segment bed file
my $output_dir = $ARGV[2];      # Path ot an output directory

my $softclip_blat_dir = $output_dir."/CNA_boundary_softclip_BLAT";
if (! -d $softclip_blat_dir) {
    mkdir $softclip_blat_dir;
}

open(OUT, ">$output_dir/run_BLAT.sh");
open(IN, $input_cna_bed);
my @in = <IN>;
close IN;

my $CNA_num = $#in + 1;

for(my $i=1; $i<=$CNA_num; $i++) {
	print OUT "blat -noHead ".$ref_genome." ".$output_dir."/CNA_boundary_softclip_fa/seg_".$i."_L_softclip.fa "
        .$softclip_blat_dir."/seg_".$i."_L_softclip.psl", "\n";
	print OUT "blat -noHead ".$ref_genome." ".$output_dir."/CNA_boundary_softclip_fa/seg_".$i."_R_softclip.fa "
        .$softclip_blat_dir."/seg_".$i."_R_softclip.psl", "\n";
}

close OUT;
print STDERR "BLAT command file was created successfully: ".$output_dir."/run_BLAT.sh\n";
exit;
