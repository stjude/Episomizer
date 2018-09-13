#!/usr/bin/env perl

# This file is part of Episomizer.
# Author: Ke (Corey) Xu, PhD and Liang (Adam) Ding, PhD
# Contact: kxu101@gmail.com

use strict;
use warnings;

if (@ARGV == 0) {
    print STDERR "Usage:\n";
    print STDERR "  SV_softclip.pl INPUT_CNA_BED FLANK SOFTCLIP_BLAT_DIR OUTPUT_DIR\n";
    exit 1;
}

my $input_cna_bed = $ARGV[0];       # Path to an input CNA segment bed file
my $flank = $ARGV[1];               # 1000 (default)
my $softclip_blat_dir = $ARGV[2];   # Path to the output directory created in blat softclip reads
my $output_dir = $ARGV[3];          # Path ot an output directory

open(IN_0, $input_cna_bed);
my @in0 = <IN_0>;
close IN_0;
my $segnum = $#in0 + 1;    # segment number

open(OUT1, ">$output_dir/matrix_softclip.txt");

my @files = ();
for (my $f=1; $f<=$segnum; $f++) {
	my $F1 = $f."_L";
	my $F2 = $f."_R";
	push @files, $F1;
	push @files, $F2;	
}

#print join("\t", @files),"\n";

print OUT1 "Matrix";
for(my $c=1; $c<=$segnum; $c++) {
	print OUT1 "	".$c."_L";
	print OUT1 "	".$c."_R";
}
print OUT1 "\n";

foreach my $file (@files) {
	my @array = (0) x ($segnum*2);
	my $input1 = $softclip_blat_dir."/seg_".$file."_softclip.psl";
	open(IN_1, $input1); 
	my @in1 = <IN_1>;
	close IN_1;

	for (my $i=0; $i<=$#in0; $i++) {
		my @row = split(/\t/, $in0[$i]);
	
		#segment left boundry	
		my %readsID = ();
		for (my $j=0; $j<=$#in1; $j++) {
			my @tmp = split(/\t/, $in1[$j]);
			if('chr'.$tmp[13] eq $row[0]) {
				if(((($tmp[15] >= $row[1] - $flank) && ($tmp[15] <= $row[1] + $flank))||(($tmp[16] >= $row[1] - $flank) && ($tmp[16] <= $row[1] + $flank))) && (! exists $readsID{$tmp[9]})) {
					$array[$i*2]++;
					$readsID{$tmp[9]} = 'just_a_value_for_the_key';  
				}				
			}		
		}
	
		#segment right boundry
		%readsID = ();
		for (my $j=0; $j<=$#in1; $j++) {
			my @tmp = split(/\t/, $in1[$j]);
			if('chr'.$tmp[13] eq $row[0]) {
				if(((($tmp[15] >= $row[2] - $flank) && ($tmp[15] <= $row[2] + $flank))||(($tmp[16] >= $row[2] - $flank) && ($tmp[16] <= $row[2] + $flank))) && (! exists $readsID{$tmp[9]})) {
					$array[$i*2+1]++;
					$readsID{$tmp[9]} = 'just_a_value_for_the_key';						
				}				
			}		
		}
	}

	print OUT1 $file,"	";
	print OUT1 join("\t", @array),"\n";
}

close OUT1;
print STDERR "Read count matrix file was created successfully: ".$output_dir."/matrix_softclip.txt\n";
exit;
