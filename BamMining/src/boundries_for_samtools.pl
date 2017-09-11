$input1 = "noCREST_copygain_LR3.txt";
$output1 = "samtools_copygainLR3_boundry_50bp.sh";

open(IN_1, $input1); 
@in1 = <IN_1>; 
close IN_1;

open(OUT1, ">$output1");

for ($i=0; $i<=$#in1; $i++) {
	chop $in1[$i];
	@row = split(/\t/, $in1[$i]);
	@field = split(/hr/, $row[0]);
	print OUT1 "samtools view /rgs01/pcgp1_bams/SJHGG/SJHGG019_S-TB-08-1210.bam $field[1]:", $row[1]-50, "-" ,$row[1]+50, " -o seg_", $i+1, "_L\n";
	print OUT1 "samtools view /rgs01/pcgp1_bams/SJHGG/SJHGG019_S-TB-08-1210.bam $field[1]:", $row[2]-50, "-" ,$row[2]+50, " -o seg_", $i+1, "_R\n";	
}

close OUT1;
exit;
