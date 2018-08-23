#!/usr/bin/env perl

$flank = 1000;
@array = (0) x 60;

#print join("\t", @array),"\n";

$input0 = "noCREST_copygain_LR3.txt"; 
$input1 = $ARGV[0];
$output1 = $ARGV[1];

open(IN_0, $input0); 
@in0 = <IN_0>; 
close IN_0;

open(IN_1, $input1); 
@in1 = <IN_1>; 
close IN_1;

open(OUT1, ">$output1");

for ($i=0; $i<=$#in0; $i++) {
	@row = split(/\t/, $in0[$i]);
	
	#segment left boundry	
	my %readsID = ();
	for ($j=0; $j<=$#in1; $j++) {
		@tmp = split(/\t/, $in1[$j]);		
		if($tmp[13] eq $row[0]) {
			if(($tmp[15] >= $row[1] - $flank) && ($tmp[15] <= $row[1] + $flank) && (! exists $readsID{$tmp[9]})) {
				$array[$i*2]++;
				$readsID{$tmp[9]} = 'just_a_value';  # the read is already matched to this boundry ONCE, so it should be excluded for further check
			}				
		}		
	}
	
	#segment right boundry
	my %readsID = ();
	for ($j=0; $j<=$#in1; $j++) {
		@tmp = split(/\t/, $in1[$j]);		
		if($tmp[13] eq $row[0]) {
			if(($tmp[15] >= $row[2] - $flank) && ($tmp[15] <= $row[2] + $flank) && (! exists $readsID{$tmp[9]})) {
				$array[$i*2+1]++;
				$readsID{$tmp[9]} = 'just_a_value';						
			}				
		}		
	}

	 	
}

@name = split(/\//, $input1);
@name1 = split(/_sof/, $name[1]);
#print $name1[0],"\n";

print OUT1 $name1[0],"	";
print OUT1 join("\t", @array),"\n";




close OUT1;
exit;
