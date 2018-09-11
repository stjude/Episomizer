#!/hpcf/apps/perl/install/5.10.1/bin/perl

#This file is part of Episomizer.

#Author: Ke (Corey) Xu, PhD
#Contact: kxu101@gmail.com


$input0 = $ARGV[0];     # CNA_region_refined.bed
$flank = $ARGV[1];      # 1000 (default)
$output1 = $ARGV[2];    # matrix_softclip.txt

open(IN_0, $input0); 
@in0 = <IN_0>; 
close IN_0;
$segnum = $#in0 + 1;    # segment number

open(OUT1, ">$output1");

$dir = "../trace/CNA_boundary_softclip_BLAT/";

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
	$input1 = $dir."seg_".$file."_softclip.psl";
	open(IN_1, $input1); 
	@in1 = <IN_1>; 
	close IN_1;

	for ($i=0; $i<=$#in0; $i++) {
		@row = split(/\t/, $in0[$i]);
	
		#segment left boundry	
		my %readsID = ();
		for ($j=0; $j<=$#in1; $j++) {
			@tmp = split(/\t/, $in1[$j]);		
			if('chr'.$tmp[13] eq $row[0]) {
				if(((($tmp[15] >= $row[1] - $flank) && ($tmp[15] <= $row[1] + $flank))||(($tmp[16] >= $row[1] - $flank) && ($tmp[16] <= $row[1] + $flank))) && (! exists $readsID{$tmp[9]})) {
					$array[$i*2]++;
					$readsID{$tmp[9]} = 'just_a_value_for_the_key';  
				}				
			}		
		}
	
		#segment right boundry
		my %readsID = ();
		for ($j=0; $j<=$#in1; $j++) {
			@tmp = split(/\t/, $in1[$j]);		
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
exit;
