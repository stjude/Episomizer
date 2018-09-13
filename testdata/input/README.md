# Example Input Files
Input files of two tumor samples from a brain tumor patient. For each sample, there are two bed files 
for the highly amplified genomic regions: CNA_region_raw_\*.bed and CNA_region_refined_\*.bed.

## Input File Descriptions
* `CNA_region_raw_D.bed`: the highly amplified segments extracted from 
[CONSERTING](https://www.nature.com/articles/nmeth.3394) somatic copy number alteration (SCNA) output
of the diagnosis sample.
* `CNA_region_raw_R.bed`: the highly amplified segments extracted from 
[CONSERTING](https://www.nature.com/articles/nmeth.3394) somatic copy number alteration (SCNA) output 
of the relapse sample.
* `CNA_region_refined_D.bed`: refined segment boundaries based on manual inspection of each segment’s 
coverage on IGV and the Blat output of the diagnosis sample.
* `CNA_region_refined_R.bed`: refined segment boundaries based on manual inspection of each segment’s 
coverage on IGV and the Blat output of the relapse sample.
* `mini_SJHGG019_E.bam`: mini bam for the diagnosis sample.
* `mini_SJHGG019_E.bam.bai`: index file for the mini bam of the diagnosis sample.
* `mini_SJHGG019_S.bam`: mini bam for the relapse sample.
* `mini_SJHGG019_S.bam.bai`: index file for the mini bam of the relapse sample.