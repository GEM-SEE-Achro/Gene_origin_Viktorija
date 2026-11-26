#!/usr/bin/env python3
import requests
import time
from Bio import SeqIO
import sys
import json

import requests

# Input and output files
fasta_file = snakemake.input.cogv
output_file = snakemake.output.res

# Extract parameters
disc_threshold = snakemake.params.discovery_threshold
min_match = snakemake.params.min_exact_match
labels = snakemake.params.node_labels

sequences = []
sequences_ids = []
for record in SeqIO.parse(fasta_file, "fasta"):
    sequences.append(str(record.seq))
    sequences_ids.append(record.id)

# Metagraph API interaction functions
# How often to retry a search the server refused with HTTP 429 (too many requests), and the first wait in seconds
MAX_RETRIES = 6
RETRY_WAIT = 10

# Submit a search, retrying with longer waits while the server answers HTTP 429 (too many requests)
def submit_with_retry(payload, sequence_id):
    wait = RETRY_WAIT
    for attempt in range(MAX_RETRIES + 1):
        response = requests.post("https://metagraph.ethz.ch:8081/search", json=payload)
        if response.status_code != 429 or attempt == MAX_RETRIES:
            return response
        # Use the server's Retry-After time if it gives one, otherwise wait longer after each try
        retry_after = response.headers.get("Retry-After", "")
        pause = int(retry_after) if retry_after.isdigit() else wait
        print(f"  {sequence_id}: HTTP 429 (too many requests), retrying in {pause} s")
        time.sleep(pause)
        wait *= 2

# Query Metagraph databases with a sequence and return the search_id
def query_metagraph(sequence, sequence_id):
    response = submit_with_retry(
        {
            "queries": [
                {
                    "db": "sra-microbe",
                    "q": sequence,
                    "params":  {
                        "discovery_threshold" : disc_threshold,
                        "min_exact_match" : min_match
                    }
                },
                {
                    "db": "refseq",
                    "q": sequence,
                    "params":  {
                        "discovery_threshold" : disc_threshold,
                        "min_exact_match" : min_match
                    }
                },
                {
                    "db": "sra-logan-chunks",
                    "q": sequence,
                    "params":  {
                        "discovery_threshold" : disc_threshold,
                        "min_exact_match" : min_match,
                        "node_labels" : labels
                    }
                },
            ],
            "search_name": f"{sequence_id} search"
        },
        sequence_id
    )

    print(f"  {sequence_id}: HTTP {response.status_code}")
    response_data = response.json()

    if "search_id" not in response_data:
        print(f"  Response: {json.dumps(response_data)[:300]}")
        raise RuntimeError(f"No search_id in response for {sequence_id}")
    
    return response_data["search_id"]

# Monitor the search status until it is done, then return the final status
def monitor_search(search_id):
    while True:
        try:
            status = requests.get(
                f"https://metagraph.ethz.ch:8081/search/{search_id}/status",
            ).json()

            if status['status'] in ['done', 'completed', 'failed']:
                return status['status']
        
        except Exception as e:
            print(f"  Error in status check: {e}")
    
        time.sleep(5)

# Get the results of a completed search
def get_results(search_id):
    results = requests.get(
        f"https://metagraph.ethz.ch:8081/search/{search_id}/results",
    ).json()
    
    return results

all_results = []

# Main loop to process each sequence: submit search, monitor status, and retrieve results
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

# Genes were sent but no search succeeded (e.g. server errors): stop with an error instead of
# writing an empty result, so Snakemake marks this step as failed
if sequences and not all_results:
    sys.exit(f"All {len(sequences)} MetaGraph queries failed, no results to write. See the messages above.")

with open(output_file, "w") as f:
    json.dump(all_results, f, indent=2)
