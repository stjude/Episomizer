#!/usr/bin/env perl

# This file is part of Episomizer.
# Author: Ke (Corey) Xu, PhD and Liang (Adam) Ding, PhD
# Contact: kxu101@gmail.com

use strict;
use warnings;

if (@ARGV == 0) {
    print STDERR "Usage:\n";
    print STDERR "  SV_bridge.pl INPUT_CNA_BED TLEN DISTANCE CNA_BOUNDARY_DIR OUTPUT_DIR\n";
    exit 1;
}

my $input_cna_bed = $ARGV[0]; 		# Path to an input CNA segment bed file
my $TLEN = $ARGV[1];     		    # 800 (default)
my $distance = $ARGV[2]; 		    # 10000 (default)
my $cna_boundary_dir = $ARGV[3];    # Path to the output directory created in extracting boundary reads using samtools
my $output_dir = $ARGV[4];  		# Path ot an output directory

open(CNA, $input_cna_bed);
my @a01 = <CNA>;
close CNA;
my $segnum = $#a01 + 1;      # segment number

open(OUT1, ">$output_dir/matrix_bridge.txt");

#opendir(DIR, $dir) or die 'no such directory';
#@filenames = grep(/seg.*psl/, readdir(DIR));
#@files = ($filenames[1],$filenames[2],$filenames[3]);
#closedir(DIR);

my @files = ();
for (my $f=1; $f<=$segnum; $f++) {
	my $F1 = $f."_L";
	my $F2 = $f."_R";
	push @files, $F1;
	push @files, $F2;	
}

#@files = ($files[1],$files[2],$files[3]);
#print join("\t", @files),"\n";


print OUT1 "Matrix";
for(my $c=1; $c<=$segnum; $c++) {
	print OUT1 "	".$c."_L";
	print OUT1 "	".$c."_R";
}
print OUT1 "\n";

foreach my $file0 (@files) {
	my @array = (0) x ($segnum*2);
	#print $file0,"\n";
	my $input0 = $cna_boundary_dir."/seg_".$file0;
	open(IN_0, $input0); 
	my @in0 = <IN_0>;
	close IN_0;
	
	my $index=0;
	foreach my $file1 (@files) {
		#print $file1,"\n";		
		my $input1 = $cna_boundary_dir."/seg_".$file1;
		open(IN_1, $input1); 
		my @in1 = <IN_1>;
		close IN_1;

		for (my $i=0; $i<=$#in0; $i++) {
			my $flag=0;
			my @row = split(/\t/, $in0[$i]);
			if(($row[6] eq "=") && (abs($row[8]) > $TLEN)) {
				for (my $j=0; $j<=$#in1; $j++) {
					my @tmp = split(/\t/, $in1[$j]);
					if(($tmp[6] eq "=") && (abs($tmp[8]) > $TLEN)) {		
						if(($tmp[2] eq $row[2]) && (abs($tmp[7] - $row[7]) < $distance)) {
							$flag = 1;							
						}
					}
					if($tmp[6] ne "=") {		                                              
						if (($tmp[6] eq $row[2]) && (abs($tmp[7] - $row[7]) < $distance)) {   
							$flag = 1;
						}
					}				
				}			 	
			}
			if($row[6] ne "=") {
				for (my $k=0; $k<=$#in1; $k++) {
					my @tmp2 = split(/\t/, $in1[$k]);
					if($tmp2[6] ne "=") {		
						if(($tmp2[6] eq $row[6]) && (abs($tmp2[7] - $row[7]) < $distance)) {
							$flag = 1;					
						} 
					}
					if(($tmp2[6] eq "=") && (abs($tmp2[8]) > $TLEN)) {	                       	
						if(($tmp2[2] eq $row[6]) && (abs($tmp2[7] - $row[7]) < $distance)) {   
							$flag = 1;					
						} 
					}						
				}				
			}
			
			if($flag==1) {
				$array[$index]++;
			}
		}
	$index++;		 	
	}
	
	#@name1 = split(/_sof/, $file0);
	#print $name1[0],"\n";

	print OUT1 $file0,"	";
	print OUT1 join("\t", @array),"\n";
}

close OUT1;
print STDERR "Read count matrix file was created successfully: ".$output_dir."/matrix_bridge.txt\n";
exit;
