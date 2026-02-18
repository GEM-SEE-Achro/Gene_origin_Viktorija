from Bio import SeqIO
import sys

input_type = sys.argv[1]
input_fasta = sys.argv[2]

bakta_db_type = sys.argv[3]
bakta_db_update = sys.argv[4]
bakta_db_threads = sys.argv[5]

abricate_mincov = sys.argv[6]
abricate_minid = sys.argv[7]
abricate_threads = sys.argv[8]

eggnog_threads = sys.argv[9]

metagraph_threads = sys.argv[10]

try:
    with open(input_fasta, "r") as handle:
        records = list(SeqIO.parse(handle, "fasta"))
        
        if len(records) == 0:
            print(f"{input_fasta}: No sequences found in the input FASTA file or file is not in valid FASTA format.")
            sys.exit(1)
        
except FileNotFoundError:
    print(f"{input_fasta}: File not found.")
    sys.exit(1)
except Exception as e:
    print(f"{input_fasta}: Error reading FASTA file: {e}")
    sys.exit(1)

if input_type not in ["fasta"]:
    print(f"{input_type}: Unsupported input type. Supported types are: fasta.")
    sys.exit(1)

if bakta_db_type not in ["light", "full"]:
    print(f"{bakta_db_type}: Unsupported Bakta database type. Supported types are: light, full.")
    sys.exit(1)

if bakta_db_update not in ["True", "False"]:
    print(f"{bakta_db_update}: Unsupported Bakta database update option. Supported options are: True, False.")
    sys.exit(1)

if not bakta_db_threads.isdigit() or int(bakta_db_threads) <= 0:
    print(f"{bakta_db_threads}: Invalid number of threads for Bakta. Please provide a positive integer.")
    sys.exit(1)

if not abricate_mincov.isdigit() or int(abricate_mincov) < 0 or int(abricate_mincov) > 100:
    print(f"{abricate_mincov}: Invalid minimum coverage for Abricate. Please provide an integer between 0 and 100.")
    sys.exit(1)

if not abricate_minid.isdigit() or int(abricate_minid) < 0 or int(abricate_minid) > 100:
    print(f"{abricate_minid}: Invalid minimum identity for Abricate. Please provide an integer between 0 and 100.")
    sys.exit(1)

if not abricate_threads.isdigit() or int(abricate_threads) <= 0:
    print(f"{abricate_threads}: Invalid number of threads for Abricate. Please provide a positive integer.")
    sys.exit(1)

if not eggnog_threads.isdigit() or int(eggnog_threads) <= 0:
    print(f"{eggnog_threads}: Invalid number of threads for EggNOG. Please provide a positive integer.")
    sys.exit(1)

if not metagraph_threads.isdigit() or int(metagraph_threads) <= 0:
    print(f"{metagraph_threads}: Invalid number of threads for MetaGraph. Please provide a positive integer.")
    sys.exit(1)