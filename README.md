# Tool development to identify gene origin and closest organisms carrying the genes

This project is to build a tool that (1) determines the likely origin of a gene/a set of genes and (2) finds the closest organisms that carry it. The tool should be built using a snakemake/nextflow pipeline. 

## Problem:

Given one or more query gene sequences (DNA or protein), determine:
- the most likely taxonomic origin (species/genus/family) of the gene,
- the closest organismal matches carrying homologous sequences,
- whether the gene is chromosomal, plasmid-borne, or mobile (i.e., potential horizontal gene transfer),
- and report what evidence supports the origin assignment.

## Aim: 

Produce an automated, reproducible pipeline that:
- takes query sequences (*what formats? DNA or protein? How to accept multiple genes as input?*),
- searches comprehensive reference databases to find homologs (*what tools could be used to maximise the efficiency and minimise the time for running the tool?*, *how to avoid donwloading huge databases and use online tools instead?*),
- reports closest organisms, sequence identity/coverage, and contextual evidence (synteny, mobile elements),
- outputs human- and machine-readable reports (TSV + summary).

## Tasks: 

1. Make a testing dataset that would contain known bacterial, plasmid, mobile genetic element genes from different species and genus.
2. Input handling:
   - accept nucleotide or protein; translate ORFs if needed.
   - check sequence composition (*can you make any assumtions from it?*)
3. Fast homology search:
   - search against large databases (DIAMOND vs NCBI nr/RefSeq, or mmseqs2) to get candidate homologs quickly (*what thresholds should be used?*)
   - search other known databases for the genes (mobile genetic elements/plasmids/genomic islands)
4. Context analysis:
   - if query originates from a genome contig: examine neighboring genes (synteny), plasmid markers (mob-suite), integrases, transposases (*what can you tell from the neighboring genes?*)
5. Report generation:
   - summarized TSV/JSON with top hits, taxonomic assignments, percent identity/coverage, synteny diagram (?).
6. Validation / benchmarking
   - test with known genes (positive controls), simulated HGT events, and negative controls.

## Tools that might be useful:
- [Branchwater sourmash](https://branchwater.jgi.doe.gov/)
- [Logan](https://logan-search.org/)
- [Pebblescout](https://pebblescout.ncbi.nlm.nih.gov/)
- [DIAMOND](https://github.com/bbuchfink/diamond)
- [GTDB-Tk](https://github.com/Ecogenomics/GTDBTk)
- [skani](https://github.com/bluenote-1577/skani)
- [MobileElementFinder](https://pypi.org/project/MobileElementFinder/)
- [ISfinder](https://www-is.biotoul.fr/)
- [Bakta](https://pubmed.ncbi.nlm.nih.gov/34739369/)
- [Eggnog](http://eggnog-mapper.embl.de/)
- [gggenes](https://wilkox.org/gggenes/)
- [pyGenomeViz](https://github.com/moshi4/pyGenomeViz)

## Literature for inspiration:

- [A framework for identifying the recent origins of mobile antibiotic resistance genes](https://www.nature.com/articles/s42003-020-01545-5)
- [SOCfinder: a genomic tool for identifying social genes in bacteria](https://pmc.ncbi.nlm.nih.gov/articles/PMC10763506/)
