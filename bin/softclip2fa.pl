#!/hpcf/apps/perl/install/5.10.1/bin/perl

#This file is part of Episomizer.

#Author: Ke (Corey) Xu, PhD
#Contact: kxu101@gmail.com


$input1 = $ARGV[0];
$output1 = $ARGV[1];

open(IN_1, $input1); 
@in1 = <IN_1>; 
close IN_1;

open(OUT1, ">$output1");

for ($i=0; $i<=$#in1; $i++) {
	chop $in1[$i];
	@row = split(/\t/, $in1[$i]);
	#@field = split(/hr/, $row[0]);
	if($row[5] =~ m/S/) {
		if(($row[10] =~ m/^#/)&&($row[10] =~ m/#$/)) {
			$pound = "poundboth";			
		} elsif ($row[10] =~ m/^#/) {
			$pound = "poundfront";			
		} elsif ($row[10] =~ m/#$/) {
			$pound = "poundend";	
		} elsif ($row[10] =~ m/#/) {
			$pound = "poundmiddle";
		} else {
			$pound = "nopound";
		}
				
		print OUT1 ">".$row[0]."__".$row[1]."__".$row[2]."__".$row[3]."__".$row[4]."__".$row[5]."__".$pound, "\n";
		print OUT1 $row[9], "\n";
	}
	
}

close OUT1;
exit;
