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

metagraph_threads = snakemake.params.metagraph_threads

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

if bakta_db_update not in [True, False]:
    sys.exit(f"{bakta_db_update}: Unsupported Bakta database update option. Supported options are: true, false.")

for name, value in [
    ("Bakta", bakta_db_threads),
    ("Abricate", abricate_threads),
    ("EggNOG", eggnog_threads),
    ("MetaGraph", metagraph_threads)
]:
    if not isinstance(value, int) or value <= 0:
        sys.exit(f"{value}: Invalid number of threads for {name}. Please provide a positive integer.")

for name, value in [
    ("minimum coverage", abricate_mincov),
    ("minimum identity", abricate_minid)
]:
    if not isinstance(value, (int, float)) or value < 0 or value > 100:
        sys.exit(f"{value}: Invalid {name} for Abricate. Please provide an integer between 0 and 100.")

Path(snakemake.output.pass_flag).touch()