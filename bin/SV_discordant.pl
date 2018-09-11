#!/hpcf/apps/perl/install/5.10.1/bin/perl

#This file is part of Episomizer.

#Author: Ke (Corey) Xu, PhD
#Contact: kxu101@gmail.com


$input0 = $ARGV[0];     # CNA_region_refined.bed
$TLEN = $ARGV[1];       # 800 (default)
$flank = $ARGV[2];      # 1000 (default)
$output1 = $ARGV[3];    # matrix_discordant.txt

open(IN_0, $input0); 
@in0 = <IN_0>; 
close IN_0;
$segnum = $#in0 + 1;    # segment number

open(OUT1, ">$output1");

$dir = "../trace/CNA_boundary_reads/";

@files = ();
for ($f=1; $f<=$segnum; $f++) {
	$F1 = $f."_L";
	$F2 = $f."_R";
	push @files, $F1;
	push @files, $F2;	
}

#print join("\t", @files),"\n";


print OUT1 "Matrix";
for($c=1; $c<=$segnum; $c++) {
	print OUT1 "	".$c."_L";
	print OUT1 "	".$c."_R";
}
print OUT1 "\n";

foreach $file (@files) {
	@array = (0) x ($segnum*2);
	#print $file0,"\n";
	$input1 = $dir."seg_".$file;
	open(IN_1, $input1); 
	@in1 = <IN_1>; 
	close IN_1;
	

	for ($i=0; $i<=$#in0; $i++) {
		@row = split(/\t/, $in0[$i]);
	
		#segment left boundry			
		for ($j=0; $j<=$#in1; $j++) {
			@tmp = split(/\t/, $in1[$j]);		
			if('chr'.$tmp[2] eq $row[0]) {
				if(($tmp[6] eq "=") && (abs($tmp[8]) > $TLEN) && ($tmp[7] >= $row[1] - $flank) && ($tmp[7] <= $row[1] + $flank)) {
					$array[$i*2]++;					
				}				
			} else {
				if(('chr'.$tmp[6] eq $row[0]) && ($tmp[7] >= $row[1] - $flank) && ($tmp[7] <= $row[1] + $flank)) {
					$array[$i*2]++;					
				}
			}		
		}
	
		#segment right boundry		
		for ($j=0; $j<=$#in1; $j++) {
			@tmp = split(/\t/, $in1[$j]);		
			if('chr'.$tmp[2] eq $row[0]) {
				if(($tmp[6] eq "=") && (abs($tmp[8]) > $TLEN) && ($tmp[7] >= $row[2] - $flank) && ($tmp[7] <= $row[2] + $flank)) {
					$array[$i*2+1]++;
				}				
			} else {
				if(('chr'.$tmp[6] eq $row[0]) && ($tmp[7] >= $row[2] - $flank) && ($tmp[7] <= $row[2] + $flank)) {
					$array[$i*2+1]++;					
				}
			}		
		}
	 	
	}

	#@name1 = split(/_sof/, $file0);
	#print $name1[0],"\n";

	print OUT1 $file,"	";
	print OUT1 join("\t", @array),"\n";
	
}

close OUT1;
exit;
