from Bio import SeqIO
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

Path(snakemake.output.pass_flag).touch()