#!/hpcf/apps/perl/install/5.10.1/bin/perl

#This file is part of Episomizer.

#Author: Ke (Corey) Xu, PhD
#Contact: kxu101@gmail.com


$CNA_file = $ARGV[0];     # CNA_region_refined.bed
$TLEN = $ARGV[1];         # 800 (default)
$distance = $ARGV[2];     # 10000 (default)
$output1 = $ARGV[3];      # matrix_bridge.txt

open(CNA, $CNA_file);
@a01 = <CNA>;
close CNA;
$segnum = $#a01 + 1;      # segment number

open(OUT1, ">$output1");

$dir = "../trace/CNA_boundary_reads/";
#opendir(DIR, $dir) or die 'no such directory';
#@filenames = grep(/seg.*psl/, readdir(DIR));
#@files = ($filenames[1],$filenames[2],$filenames[3]);
#closedir(DIR);

@files = ();
for ($f=1; $f<=$segnum; $f++) {
	$F1 = $f."_L";
	$F2 = $f."_R";
	push @files, $F1;
	push @files, $F2;	
}

#@files = ($files[1],$files[2],$files[3]);
#print join("\t", @files),"\n";


print OUT1 "Matrix";
for($c=1; $c<=$segnum; $c++) {
	print OUT1 "	".$c."_L";
	print OUT1 "	".$c."_R";
}
print OUT1 "\n";

foreach $file0 (@files) {
	@array = (0) x ($segnum*2);
	#print $file0,"\n";
	$input0 = $dir."seg_".$file0;
	open(IN_0, $input0); 
	@in0 = <IN_0>; 
	close IN_0;
	
	$index=0;
	foreach $file1 (@files) {
		#print $file1,"\n";		
		$input1 = $dir."seg_".$file1;
		open(IN_1, $input1); 
		@in1 = <IN_1>; 
		close IN_1;

		for ($i=0; $i<=$#in0; $i++) {
			$flag=0;
			@row = split(/\t/, $in0[$i]);
			if(($row[6] eq "=") && (abs($row[8]) > $TLEN)) {
				for ($j=0; $j<=$#in1; $j++) {
					@tmp = split(/\t/, $in1[$j]);
					if(($tmp[6] eq "=") && (abs($tmp[8]) > $TLEN)) {		
						if(($tmp[2] eq $row[2]) && (abs($tmp[7] - $row[7]) < $distance)) {
							$flag = 1;							
						}
					}
					if($tmp[6] ne "=") {		                                              # added this block on 2018/08/27 for SVs like TCGA-0152-D (1L - 6L)
						if (($tmp[6] eq $row[2]) && (abs($tmp[7] - $row[7]) < $distance)) {   
							$flag = 1;
						}
					}				
				}			 	
			}
			if($row[6] ne "=") {
				for ($k=0; $k<=$#in1; $k++) {
					@tmp2 = split(/\t/, $in1[$k]);
					if($tmp2[6] ne "=") {		
						if(($tmp2[6] eq $row[6]) && (abs($tmp2[7] - $row[7]) < $distance)) {
							$flag = 1;					
						} 
					}
					if(($tmp2[6] eq "=") && (abs($tmp2[8]) > $TLEN)) {	                       # added this block on 2018/08/27 for SVs like TCGA-0152-D (1L - 6L)	
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
exit;
