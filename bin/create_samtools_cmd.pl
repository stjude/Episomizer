#!/usr/bin/env perl

# Create samtools command file to extract reads around boundaries of CNA segments.
# This file is part of Episomizer.
# Author: Ke (Corey) Xu, PhD and Liang (Adam) Ding, PhD
# Contact: kxu101@gmail.com

use strict;
use warnings;

if (@ARGV == 0) {
    print STDERR "Usage:\n";
    print STDERR "  create_samtools_cmd.pl INPUT_BAM INPUT_CNA_BED OUTPUT_DIR\n";
    exit 1;
}

my $buffer = 50;               # Number of nucelotides to examine around each boundary (default is 50bp)
my $input_bam = $ARGV[0];      # Path to an input tumor bam
my $input_cna_bed = $ARGV[1];  # Path to an input CNA segment bed file
my $output_dir = $ARGV[2];     # Path ot an output directory

my $cna_boundary_dir = $output_dir."/CNA_boundary_reads";
if (! -d $cna_boundary_dir) {
    mkdir $cna_boundary_dir;
}

open(IN_1, $input_cna_bed);
my @in1 = <IN_1>;
close IN_1;

open(OUT1, ">$output_dir"."/run_samtools.sh");

# Create a file with each line a samtools command
for (my $i=0; $i<=$#in1; $i++) {
	chop $in1[$i];
	my @row = split(/\t/, $in1[$i]);
	my @field = split(/hr/, $row[0]);
	print OUT1 "samtools view ".$input_bam." $field[1]:", $row[1]-$buffer, "-" ,$row[1]+$buffer,
        " -o ".$cna_boundary_dir."/seg_", $i+1, "_L\n";
	print OUT1 "samtools view ".$input_bam." $field[1]:", $row[2]-$buffer, "-" ,$row[2]+$buffer,
        " -o ".$cna_boundary_dir."/seg_", $i+1, "_R\n";
}

close OUT1;
print STDERR "Samtools command file was created successfully: ".$output_dir."/run_samtools.sh\n";
exit;