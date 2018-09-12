# Usage Example
This is an example to use Episomizer to construct double minutes on the mini-bam file created by 
down-sampling on the relapse sample (SJHGG019_S). For general usage information, 
see the home page [Episomizer](#Episomizer).

# Setting Environment
Set `$EPISOMIZER_HOME` to the cloned directory, add bin path to `$PATH` and enter `$EPISOMIZER_HOME`
directory.
```
$ EPISOMIZER_HOME=<path_to_cloned_dir>
$ export PATH=$EPISOMIZER_HOME/bin:$PATH
$ cd $EPISOMIZER_HOME
```

# Procedures
**Step 1:** Determine a threshold for highly amplified genomic segments based on the copy number data 
(we used Log2Ratio > 4 based on the [CONSERTING](https://www.nature.com/articles/nmeth.3394) Log2Ratio 
distribution).

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