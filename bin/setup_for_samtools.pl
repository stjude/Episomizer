#!/hpcf/apps/perl/install/5.10.1/bin/perl

#This file is part of Episomizer.

#Author: Ke (Corey) Xu, PhD
#Contact: kxu101@gmail.com


$buffer = 50;           # number of nucelotides to examine around each boundary (default is 50bp)

my $dir1 = "../trace/CNA_boundary_reads";
my $dir2 = "../trace/CNA_boundary_softclip_fa";
my $dir3 = "../trace/CNA_boundary_softclip_BLAT";

mkdir $dir1;
mkdir $dir2;
mkdir $dir3;

$bam_file = $ARGV[0];   # /research/rgs01/reference/restricted/PCGP/GRCh37-lite/WHOLE_GENOME/SJHGG019_S.bam
$input1 = $ARGV[1];     # CNA_region_refined.bed
$output1 = $ARGV[2];    # run_samtools.sh

open(IN_1, $input1); 
@in1 = <IN_1>; 
close IN_1;

open(OUT1, ">$output1");

for ($i=0; $i<=$#in1; $i++) {
	chop $in1[$i];
	@row = split(/\t/, $in1[$i]);
	@field = split(/hr/, $row[0]);
	print OUT1 "samtools view ".$bam_file." $field[1]:", $row[1]-$buffer, "-" ,$row[1]+$buffer, " -o ../trace/CNA_boundary_reads/seg_", $i+1, "_L\n";
	print OUT1 "samtools view ".$bam_file." $field[1]:", $row[2]-$buffer, "-" ,$row[2]+$buffer, " -o ../trace/CNA_boundary_reads/seg_", $i+1, "_R\n";	
}

close OUT1;
exit;
