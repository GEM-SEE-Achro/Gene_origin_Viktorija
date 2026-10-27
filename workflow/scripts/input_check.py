from Bio import SeqIO
import re
import sys
from pathlib import Path

# All the input files and parameters
input_type = snakemake.params.input_type
input_fasta = snakemake.params.input_fasta

bakta_db_type = snakemake.params.bakta_db_type
bakta_db_update = snakemake.params.bakta_db_update
bakta_db_threads = snakemake.params.bakta_db_threads

abricate_mincov = snakemake.params.abricate_mincov
abricate_minid = snakemake.params.abricate_minid
abricate_threads = snakemake.params.abricate_threads

eggnog_threads = snakemake.params.eggnog_threads

genomad_threads = snakemake.params.genomad_threads

metagraph_run = snakemake.params.metagraph_run
metagraph_threads = snakemake.params.metagraph_threads
metagraph_discovery_threshold = snakemake.params.metagraph_discovery_threshold
metagraph_min_exact_match = snakemake.params.metagraph_min_exact_match
metagraph_node_labels = snakemake.params.metagraph_node_labels

select_groups = snakemake.params.select_groups
select_genes = snakemake.params.select_genes
select_regions = snakemake.params.select_regions
sample_names = snakemake.params.sample_names

# Checking if the input FASTA file exists and is in valid format
try:
    with open(input_fasta, "r") as handle:
        records = list(SeqIO.parse(handle, "fasta"))
        
        if len(records) == 0:
            sys.exit(f"{input_fasta}: No sequences found in the input FASTA file or file is not in valid FASTA format.")
        
except FileNotFoundError:
    sys.exit(f"{input_fasta}: File not found.")
except Exception as e:
    sys.exit(f"{input_fasta}: Error reading FASTA file: {e}")

# Validating input parameters
if input_type not in ["fasta"]:
    sys.exit(f"{input_type}: Unsupported input type. Supported types are: fasta.")

if bakta_db_type not in ["light", "full"]:
    sys.exit(f"{bakta_db_type}: Unsupported Bakta database type. Supported types are: light, full.")

# isinstance(..., bool) instead of "in [True, False]", because 1 == True and 0 == False in Python
if not isinstance(bakta_db_update, bool):
    sys.exit(f"{bakta_db_update}: Unsupported Bakta database update option. Supported options are: true, false.")

if not isinstance(metagraph_run, bool):
    sys.exit(f"{metagraph_run}: Unsupported MetaGraph run option. Supported options are: true, false.")

# bool is excluded explicitly, because True/False also count as int in Python
for name, value in [
    ("Bakta", bakta_db_threads),
    ("Abricate", abricate_threads),
    ("EggNOG", eggnog_threads),
    ("geNomad", genomad_threads),
    ("MetaGraph", metagraph_threads)
]:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        sys.exit(f"{value}: Invalid number of threads for {name}. Please provide a positive integer.")

for name, value in [
    ("minimum coverage", abricate_mincov),
    ("minimum identity", abricate_minid)
]:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0 or value > 100:
        sys.exit(f"{value}: Invalid {name} for Abricate. Please provide a number between 0 and 100.")

for name, value in [
    ("discovery threshold", metagraph_discovery_threshold),
    ("minimum exact match", metagraph_min_exact_match)
]:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0 or value > 1:
        sys.exit(f"{value}: Invalid {name} for MetaGraph. Please provide a number between 0 and 1.")

if not isinstance(metagraph_node_labels, list) or len(metagraph_node_labels) == 0 \
        or not all(isinstance(label, str) for label in metagraph_node_labels):
    sys.exit(f"{metagraph_node_labels}: Invalid node labels for MetaGraph. Please provide a non-empty list of names.")

# MetaGraph gene selection: groups
if not isinstance(select_groups, list):
    sys.exit(f"{select_groups}: Invalid MetaGraph gene groups. Please provide a list, e.g. [\"amr\", \"cog:VX\"].")
for group in select_groups:
    if not isinstance(group, str) or not (group in ["amr", "plasmid", "virus"] or re.fullmatch(r"cog:[A-Z]+", group)):
        sys.exit(f"{group}: Unsupported MetaGraph gene group. Supported groups are: amr, plasmid, virus, cog:LETTERS (e.g. cog:VX).")

# MetaGraph gene selection: genes (a lone "*" would select every gene)
if not isinstance(select_genes, list):
    sys.exit(f"{select_genes}: Invalid MetaGraph genes. Please provide a list of gene names or locus tags.")
for gene in select_genes:
    if not isinstance(gene, str) or gene.strip() in ["", "*"]:
        sys.exit(f"{gene}: Invalid MetaGraph gene. Please provide a gene name or locus tag, optionally ending with *.")

# MetaGraph gene selection: regions, {sample: ["contig:start-end", ...]}
if not isinstance(select_regions, dict):
    sys.exit(f"{select_regions}: Invalid MetaGraph regions. Please provide sample names with lists of regions.")
for sample, regions in select_regions.items():
    if sample not in sample_names:
        sys.exit(f"{sample}: MetaGraph regions given for a sample that is not in samples.")
    if not isinstance(regions, list):
        sys.exit(f"{regions}: Invalid MetaGraph regions for {sample}. Please provide a list, e.g. [\"contig_1:100-5000\"].")
    for region in regions:
        match = re.fullmatch(r"(.+):(\d+)-(\d+)", region) if isinstance(region, str) else None
        if not match or int(match.group(2)) > int(match.group(3)):
            sys.exit(f"{region}: Invalid MetaGraph region for {sample}. Please use contig:start-end with start <= end, e.g. contig_1:100-5000.")

Path(snakemake.output.pass_flag).touch()