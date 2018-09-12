# Episomizer
Episomizer is currently a semi-automated pipeline for constructing double minutes (a.k.a. episome) 
using WGS data. The challenge to fully automate the entire process drives from the varying 
complexity of genomic rearrangements in different tumor samples.

Episomizer consists of two major components:
* Bam mining extracts highly amplified genomic segments based on the copy number data, refine the 
segment boundaries and calculates precise number of supporting reads for each manual inspected 
structure variation that links a pair of segment boundaries.
* Composer takes inputs of highly amplified somatic copy number alteration (CNA) segments and
structure variants (SV) associated with the segment boundaries, composes the segments to form simple
cycles as candidates of circular double minute structures.

## Prerequisites
* [Perl=5.10.1](https://www.perl.org/)
* [R=3.0.1](https://www.r-project.org/)
* [Samtools=1.7](http://samtools.sourceforge.net/)
* [blat=36](https://genome.ucsc.edu/FAQ/FAQblat)
* [Python=3.6](https://www.python.org/downloads/release/python-360/)
* [NetworkX=2.1](https://networkx.github.io/)
* [pybedtools=0.7.10](https://daler.github.io/pybedtools/#getting-started)

## Installation
Installation is simply cloning of the repository to a working directory and 
adding `$EPISOMIZER_HOME/bin` to `$PATH`.
```
$ EPISOMIZER_HOME=<path_to_working_dir>
$ export PATH=$EPISOMIZER_HOME/bin:$PATH
```

## Usage
```
Usage:
    episomizer <SUBCOMMAND> [args...]
Subcommands:
    create_samtools_cmd    Create samtools command file to extract reads around boundaries of CNA segments
    create_softclip2fa_cmd Create command file to extract softclip reads
    create_blat_cmd        Create command file to blat softclip reads
    SV_softclip            Create a read count matrix using softclip reads
    SV_discordant          Create a read count matrix using discordant reads
    SV_bridge              Create a read count matrix using bridging discordant reads
```
For details on how to run the semi-automated pipeline, see the following [Procedure](#Procedure) section.

## Procedure
**Step 1:** Determine a threshold for highly amplified genomic segments based on the copy number data 
(we used Log2Ratio > 4 based on the [CONSERTING](https://www.nature.com/articles/nmeth.3394) Log2Ratio 
distribution).

**Step 2:** Get the putative edges.
1. Generate the shell script with samtools commands to extract the reads around segment boundaries.
    ```
    $ episomizer create_samtools_cmd INPUT_BAM INPUT_CNA_BED OUTPUT_DIR
    ```
    Run the shell script.
    ```
    $ OUTPUT_DIR/run_samtools.sh 
    ```

2. Generate the shell script to extract softclip reads.
    ```
    $ create_softclip2fa_cmd.pl INPUT_CNA_BED OUTPUT_DIR
    ```
    Run the shell script.
    ```
    $ OUTPUT_DIR/run_softclip2fa.sh
    ```
    
3. Generate the shell script to blat the softclip reads.
    ```
    create_blat_cmd.pl REF_GENOME_BIT INPUT_CNA_BED OUTPUT_DIR
    ```
    The reference genome GRCh37-lite.2bit can be downloaded from 
    [St. Jude public FTP site](http://ftp.stjude.org/pub/software/cis-x/GRCh37-lite.2bit).
    
    Run the shell script (recommend parallel processing).
    ```
    $ OUTPUT_DIR/run_BLAT.sh
    ```
    


## Maintainers
* [Liang Ding](https://github.com/adamdingliang)
* [Ke Xu](https://github.com/FromSoSimple)