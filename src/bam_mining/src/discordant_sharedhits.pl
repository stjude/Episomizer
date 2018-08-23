#!/usr/bin/env perl

$distance = 10000;

$dir = "copygainLR3_boundry_50bp_allreads/";
#opendir(DIR, $dir) or die 'no such directory';
#@filenames = grep(/seg.*psl/, readdir(DIR));
#@files = ($filenames[1],$filenames[2],$filenames[3]);
#closedir(DIR);

@files = ();
for ($f=1; $f<=30; $f++) {
	$F1 = "seg_".$f."_L";
	$F2 = "seg_".$f."_R";
	push @files, $F1;
	push @files, $F2;	
}

#@files = ($files[1],$files[2],$files[3]);
print join("\t", @files),"\n";

$output1 = 'matrix_discordant_sharedhits.txt';
open(OUT1, ">$output1");
print OUT1 "Matrix	1_L	1_R	2_L	2_R	3_L	3_R	4_L	4_R	5_L	5_R	6_L	6_R	7_L	7_R	8_L	8_R	9_L	9_R	10_L	10_R	11_L	11_R	12_L	12_R	13_L	13_R	14_L	14_R	15_L	15_R	16_L	16_R	17_L	17_R	18_L	18_R	19_L	19_R	20_L	20_R	21_L	21_R	22_L	22_R	23_L	23_R	24_L	24_R	25_L	25_R	26_L	26_R	27_L	27_R	28_L	28_R	29_L	29_R	30_L	30_R\n";

foreach $file0 (@files) {
	@array = (0) x 60;
	#print $file0,"\n";
	$input0 = $dir.$file0;
	open(IN_0, $input0); 
	@in0 = <IN_0>; 
	close IN_0;
	
	$index=0;
	foreach $file1 (@files) {
		#print $file1,"\n";		
		$input1 = $dir.$file1;
		open(IN_1, $input1); 
		@in1 = <IN_1>; 
		close IN_1;

		for ($i=0; $i<=$#in0; $i++) {
			$flag=0;
			@row = split(/\t/, $in0[$i]);
			if((($row[6] eq "=") && (abs($row[8]) > 800))||($row[6] ne "=")) {
				for ($j=0; $j<=$#in1; $j++) {
					@tmp = split(/\t/, $in1[$j]);
					if(($tmp[6] eq "=") && (abs($tmp[8]) > 800)) {		
						if(($tmp[2] eq $row[2])&&(abs($tmp[7] - $row[7]) < $distance)) {
							$flag = 1;							
						}
					}
					if($tmp[6] ne "=") {		
						if(($tmp[6] eq $row[6])&&(abs($tmp[7] - $row[7]) < $distance)) {
							$flag = 1;							
						}
					}				
				}
				if($flag==1) {
					$array[$index]++;
				}			 	
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
exit;
