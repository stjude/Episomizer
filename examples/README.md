# Usage Example
This page shows an example of applying the procedure described in [Episomizer](../README.md) page to construct 
double minutes on the mini-bam file created by down-sampling on the relapse sample (SJHGG019_S). For the general
usage information, see [Episomizer](../README.md) home page.

## Set Environment
Set `$EPISOMIZER_HOME` to the cloned directory, add bin path to `$PATH` and enter `$EPISOMIZER_HOME`
directory.
```
$ EPISOMIZER_HOME=<path_to_cloned_dir>
$ export PATH=$EPISOMIZER_HOME/bin:$PATH
$ cd $EPISOMIZER_HOME
```

## Procedure
**Step 1:** We used Log2Ratio > 4 based on the [CONSERTING](https://www.nature.com/articles/nmeth.3394) Log2Ratio 
distribution to determine the highly amplified genomic segments 
(file [CNA_region_raw_R.bed](../testdata/input/CNA_region_raw_R.bed)). For
descriptions about all the example input files, see [input](../testdata/input/README.md) page.

**Step 2:** Get the putative edges.
1. Generate the shell script with samtools commands and the intermediate folder 
([CNA_boundary_reads](../testdata/intmd/trace/CNA_boundary_reads)) in 
    the given output directory.
    ```
    $ episomizer create_samtools_cmd ./testdata/input/mini_SJHGG019_S.bam ./testdata/input/CNA_region_raw_D.bed 
    ./testdata/intmd/trace
    Samtools commands created successfully.
    ```
    Run the shell script.
    ```
    $ ./testdata/intmd/trace/run_samtools.sh
    ```
    
2. Generate the shell script to extract softclip reads and the intermediate folder 
([CNA_boundary_softclip_fa](../testdata/intmd/trace/CNA_boundary_softclip_fa)) in
    the given output directory.
    ```
    $ episomizer create_softclip2fa_cmd ./testdata/input/CNA_region_raw_R.bed ./testdata/intmd/trace
    ```
    Run the shell script.
    ```
    $ ./testdata/intmd/trace/run_softclip2fa.sh
    ```
    
3. Generate the shell script to blat the softclip reads and the intermediate folder 
([CNA_boundary_softclip_BLAT](../testdata/intmd/trace/CNA_boundary_softclip_BLAT)) in
    the given output directory.
    ```
    $ episomizer create_blat_cmd GRCh37-lite.2bit ./testdata/input/CNA_region_raw_R.bed ./testdata/intmd/trace
    ```
    The reference genome GRCh37-lite.2bit can be downloaded from 
    [St. Jude public FTP site](http://ftp.stjude.org/pub/software/cis-x/GRCh37-lite.2bit).
    
    Run the shell script (recommend parallel processing).
    ```
    $ ./testdata/intmd/trace/run_BLAT.sh
    ```
    
4. Create 3 read count matrices using softclip reads, discordant reads and bridging discordant reads.
    ```
    $ episomizer SV_softclip ./testdata/input/CNA_region_raw_R.bed 1000 ./testdata/intmd/trace/CNA_boundary_softclip_BLAT ./testdata/intmd/trace
    $ episomizer SV_discordant ./testdata/input/CNA_region_raw_R.bed 800 1000 ./testdata/intmd/trace/CNA_boundary_reads ./testdata/intmd/trace
    $ episomizer SV_bridge ./testdata/input/CNA_region_raw_R.bed 800 1000 ./testdata/intmd/trace/CNA_boundary_reads ./testdata/intmd/trace
    ```
    
5. Produce edges to connect SVs based on read count matrices.
    ```
    $ episomizer matrix2edges ./testdata/input/CNA_region_raw_R.bed ./testdata/intmd/trace/matrix_softclip.txt ./testdata/intmd/trace/putative_edges_softclip.txt
    $ episomizer matrix2edges ./testdata/input/CNA_region_raw_R.bed ./testdata/intmd/trace/matrix_discordant.txt ./testdata/intmd/trace/putative_edges_discordant.txt
    $ episomizer matrix2edges ./testdata/input/CNA_region_raw_R.bed ./testdata/intmd/trace/matrix_bridge.txt ./testdata/intmd/trace/putative_edges_bridge.txt
    ```
 
**Step 3:** Manually review the putative edges.
Please follow the instruction in [Episomizer](../README.md) home page. The review process is summarized in 
[edges_review_relapse_rawCNA.xlsx](./testdata/intmd/reviewed_data/edges_review_relapse_rawCNA.xlsx).

**Step 4:** Compose circular double minute structures.
```
$ episomizer composer circ -c ./testdata/intmd/reviewed_data/Reviewed_segments_for_graph_relapse_rawCNA.txt -l ./testdata/intmd/reviewed_data/Reviewed_edges_for_graph_relapse_rawCNA.txt -d ./testdata/output/double_minutes_relapse.txt
```

## Notes on the diagnosis sample (SJHGG019)
We used the same workflow to generate putative edges for the diagnosis sample, but since the sequencing coverage 
for the diagnosis sample is much choppier, the SCNA segments boundaries are not as accurate as the relapse sample, 
which influenced the identification of a few SVs. After manual review of the reads and their Blat results, together 
with the Chromium data, we rescued eight missed SVs. The review process can be viewed 
at [edges_review_diagnosis_rawCNA.xlsx](../testdata/intmd/reviewed_data/edges_review_diagnosis_rawCNA.xlsx).  