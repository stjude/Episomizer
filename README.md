# Episomizer
Episomizer is currently a semi-automated pipeline for constructing double minutes (aka. episome) 
using WGS data. 

Episomizer consists of two major components:
* Bam mining extract the reads around the boundaries of highly amplified genomic regions, 
search for evidence of soft-clipped reads, discordant reads, and bridge reads that support 
putative SVs (aka. edges) between any two segment boundaries. The reported putative edges are subject 
to manual review. 
* Composer takes inputs of manually reviewed edges associated with the segment boundaries together 
with the highly amplified genomic segments, composes the segments to form simple
cycles as candidates of circular DNA structures.

## Citation
Xu, K., Ding, L., Chang, TC., Shao, Y., Chiang, J., Mulder, H., Wang, S., Shaw, T.I., Wen, J., 
Hover, L., McLeod, C., Wang, YD., Easton, J., Rusch, M., Dalton, J., Downing, J.R., Ellison, D.W., 
Zhang, J., Baker, S.J., Wu, G.
Structure and evolution of double minutes in diagnosis and relapse brain tumors.
Acta Neuropathologica, Sep 2018, DOI: [10.1007/s00401-018-1912-1](https://doi.org/10.1007/s00401-018-1912-1).

## Prerequisites
* [Perl=5.10.1](https://www.perl.org/)
* [R=3.0.1](https://www.r-project.org/)
* [Samtools=1.7](http://samtools.sourceforge.net/)
* [blat=36](https://genome.ucsc.edu/FAQ/FAQblat)
* [Python>=3.5.2](https://www.python.org/downloads/release/python-360/)
    * [NetworkX=2.1](https://networkx.github.io/)
    * [pybedtools>=0.7.0](https://daler.github.io/pybedtools/#getting-started)

## Installation
To install, simply clone of the repository to a working directory and add `$EPISOMIZER_HOME/bin` to `$PATH`.
```
$ EPISOMIZER_HOME=<path_to_working_dir>
$ export PATH=$EPISOMIZER_HOME/bin:$PATH
```

## Usage
```
Usage:
    episomizer <SUBCOMMAND> [args...]
Subcommands:
    create_samtools_cmd    Create samtools command file to extract reads around segment boundaries
    create_softclip2fa_cmd Create command file to extract softclip reads
    create_blat_cmd        Create command file to blat softclip reads
    SV_softclip            Create read count matrix for softclip reads supported SVs
    SV_discordant          Create read count matrix for discordant reads supported SVs
    SV_bridge              Create read count matrix for bridge reads supported SVs
    matrix2edges           Convert read count matrix to putative edges
    composer               Compose segments and edges to identify circular DNA structures
```
For details on how to run the semi-automated pipeline, see the following [Procedure](#Procedure) section. 
**For a concrete example of constructing double minutes on a mini-bam file, see [examples](./examples/README.md) page.**

## Procedure
**Step 1:** Determine a threshold for highly amplified genomic segments based on the empirical distribution
  of Log2Ratio of copy number data.

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
    $ episomizer create_softclip2fa_cmd INPUT_CNA_BED OUTPUT_DIR
    ```
    Run the shell script.
    ```
    $ OUTPUT_DIR/run_softclip2fa.sh
    ```
    
3. Generate the shell script to blat the softclip reads.
    ```
    $ episomizer create_blat_cmd REF_GENOME_BIT INPUT_CNA_BED OUTPUT_DIR
    ```
    **The reference genome GRCh37-lite.2bit can be downloaded from 
    [St. Jude public FTP site](http://ftp.stjude.org/pub/software/cis-x/GRCh37-lite.2bit) and can be placed under the working directory.**
    
    Run the shell script (submitting the jobs in parallel is strongly recommended).
    ```
    $ OUTPUT_DIR/run_BLAT.sh
    ```
    
 4. Create 3 read count matrices using softclip reads, discordant reads and bridging discordant reads.
    ```
    $ episomizer SV_softclip INPUT_CNA_BED FLANK SOFTCLIP_BLAT_DIR OUTPUT_DIR
    $ episomizer SV_discordant INPUT_CNA_BED TLEN FLANK BOUNDARY_READS_DIR OUTPUT_DIR
    $ episomizer SV_bridge INPUT_CNA_BED TLEN DISTANCE BOUNDARY_READS_DIR OUTPUT_DIR
    ```
    
 5. Convert matrix file to edges file.
    ```
    $ episomizer matrix2edges INPUT_CNA_BED MATRIX_FILE OUTPUT_EDGE_FILE
    ```
    
**Step 3:** Manually review the putative edges.

For all 3 types of putative edges (softclip, discordant, and bridge) from the above output, they are sorted by the total number of supporting reads from high to low. 
These putative edges need to be manually reviewed by examining the boundary reads and their Blat results in the “trace” folder, 
as well as by examining the coverage depth around the segments on IGV to refine the segment boundaries. Edges with few reads support 
on each side are usually spurious or indicate minor clones which we do not consider in our current study. The basic review process is described below:

For the softclip edges, the edges that represent adjacent segments should be annotated first. Then for the rest of the 
edges, their Blat output need to be manually reviewed to determine the orientations of two joined segments such that 
true edge will be annotated and accompanying false edges will be removed. 

For the discordant edges, the edges that are already reviewed in the softclip edges can be removed first. Then for the 
rest of the edges, their boundary reads (in SAM format) need to be manually reviewed, especially the FLAG column, to determine 
the orientations of two joined segments such that true edge will be annotated and accompanying false edges will be removed. 

For the bridge edges, the edges that are already reviewed in the softclip and discordant edges can be removed first.
Then for the rest of the edges, their boundary reads (in SAM format) need to be manually reviewed to determine if their bridging segment's 
orientation is in harmony with those of the two joined segments. True edge will be annotated and accompanying false edges will be removed. 
In addition, if the reads support from both sides are off balance (for example, AtoB is 1 but BtoA is 100), the edge is most likely to be spurious.

The reviewed edges from the 3 putative edges files are combined into one "edge" file as part of the input for the next step. 

**Step 4:** Compose circular double minute structures.
```
$ episomizer composer circ -c REVIEWED_SEGMENTS -l REVIEWED_EDGES -d OUTPUT_DOUBLE_MINUTES
```

## Maintainers
* [Liang Ding](https://github.com/adamdingliang)
* [Ke Xu](https://github.com/FromSoSimple)