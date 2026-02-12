#!/usr/bin/env python3
import requests
import time
from Bio import SeqIO
import sys
import json

fasta_file = sys.argv[1]
output_file = sys.argv[2]

sequences = []
sequences_ids = []
for record in SeqIO.parse(fasta_file, "fasta"):
    sequences.append(str(record.seq))
    sequences_ids.append(record.id)

def query_metagraph(sequence, sequence_id):
    response = requests.post(
        "https://metagraph.ethz.ch:8081/search",
        json={
            "queries": [
                {
                    "db": "sra-microbe",
                    "q": sequence,
                },
                {
                    "db": "refseq85_coord",
                    "q": sequence,
                },
            ],
            "search_name": f"{sequence_id} search"
        },
    )

    response_data = response.json()
    
    return response_data["search_id"]

def monitor_search(search_id):
    while True:
        try:
            status = requests.get(
                f"https://metagraph.ethz.ch:8081/search/{search_id}/status",
            ).json()

            if status['status'] in ['done', 'completed', 'failed']:
                return status
        
        except Exception as e:
            print(f"  Error in status check: {e}")
    
        time.sleep(5)

def get_results(search_id):
    results = requests.get(
        f"https://metagraph.ethz.ch:8081/search/{search_id}/results",
    ).json()
    
    return results

all_results = []

for i, (seq, seq_id) in enumerate(zip(sequences, sequences_ids), 1):
    try:
        search_id = query_metagraph(seq, seq_id)
    except Exception as e:
        print(f"Error submitting search for {seq_id}: {e}")
        continue
    
    try:
        status = monitor_search(search_id)
        if status in ['failed', 'timeout']:
            print(f"  Skipping due to {status}")
            continue
            
    except Exception as e:
        print(f"  Error monitoring search for {seq_id}: {e}")
        import traceback
        traceback.print_exc()
        continue
    
    try:
        results = get_results(search_id)
        
        all_results.append({
            "query_id": seq_id,
            "search_id": search_id,
            "raw_results": results
        })

    except Exception as e:
        print(f"  ERROR getting results: {e}")
        import traceback
        traceback.print_exc()
        continue

with open(output_file, "w") as f:
    json.dump(all_results, f, indent=2)
