# Usage Example
This is an example to use [Episomizer](../README.md) to construct double minutes on the mini-bam file created by 
down-sampling on the relapse sample (SJHGG019_S). For the general usage information, 
see [Episomizer](../README.md) home page.

# Set Environment
Set `$EPISOMIZER_HOME` to the cloned directory, add bin path to `$PATH` and enter `$EPISOMIZER_HOME`
directory.
```
$ EPISOMIZER_HOME=<path_to_cloned_dir>
$ export PATH=$EPISOMIZER_HOME/bin:$PATH
$ cd $EPISOMIZER_HOME
```

# Procedure
**Step 1:** We used Log2Ratio > 4 based on the [CONSERTING](https://www.nature.com/articles/nmeth.3394) Log2Ratio 
distribution to determine the highly amplified genomic segments (file `testdata/input/CNA_region_raw_D.bed`). For
descriptions about all the example input files, see [input](../testdata/input/README.md) page.

**Step 2:** Get the putative edges.
1. Generate the shell script with samtools commands and the intermediate folder (`CNA_boundary_reads`) in 
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
    
2. Generate the shell script to extract softclip reads and the intermediate folder (`CNA_boundary_softclip_fa`) in
    the given output directory.
    ```
    $ episomizer create_softclip2fa_cmd ./testdata/input/CNA_region_raw_R.bed ./testdata/intmd/trace
    ```
    Run the shell script.
    ```
    $ ./testdata/intmd/trace/run_softclip2fa.sh
    ```
    
3. Generate the shell script to blat the softclip reads.
    ```
    $ episomizer create_blat_cmd GRCh37-lite.2bit ./testdata/input/CNA_region_raw_R.bed ./testdata/intmd/trace
    ```
    The reference genome GRCh37-lite.2bit can be downloaded from 
    [St. Jude public FTP site](http://ftp.stjude.org/pub/software/cis-x/GRCh37-lite.2bit).
    
    Run the shell script (recommend parallel processing).
    ```
    $ ./testdata/intmd/trace/run_BLAT.sh
    ```