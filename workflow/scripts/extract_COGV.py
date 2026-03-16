#!/usr/bin/env python3
import sys
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

bakta_tsv = snakemake.input.bakta_tsv
eggnog_tsv = snakemake.input.eggnog_tsv
fasta_input = snakemake.input.input_fasta
fasta_output = snakemake.output.output_fasta

cogv_v_id = set()

# Reading and parsing eggnog tsv file
with open(eggnog_tsv, 'r') as f:
    lines = f.readlines()

data_start_index = 0
for i, line in enumerate(lines):
    if line.startswith('#query'):
        data_start_index = i
        break

eggnog_df = pd.read_csv(eggnog_tsv, sep='\t', skiprows=data_start_index, header=0)
cogv_eggnog_id = set(eggnog_df[eggnog_df['COG_category'] == 'V']['#query'])

# Reading and parsing bakta tsv file
with open(bakta_tsv, 'r') as f:
    lines = f.readlines()

data_start_index = 0
for i, line in enumerate(lines):
    if line.startswith('#Sequence'):
        data_start_index = i
        break

bakta_df = pd.read_csv(bakta_tsv, sep='\t', skiprows=data_start_index, header=0)
cogv_bakta_id = set(bakta_df[bakta_df['DbXrefs'].str.contains('COG:V', na=False)]['Locus Tag'])

# Extracting COG=V genes from both datasets
cogv_all_id = cogv_eggnog_id.union(cogv_bakta_id)

selected_genes = bakta_df[bakta_df['Locus Tag'].isin(cogv_all_id)]

input_sequence = SeqIO.read(fasta_input, 'fasta')
output_records = []

for _, gene in selected_genes.iterrows():
    start = gene['Start'] - 1
    end = gene['Stop']
    strand = gene['Strand']
    locus_tag = gene['Locus Tag']
    gene_name = gene['Gene']

    gene_seq = input_sequence.seq[start:end]

    if strand == '-':
        gene_seq = gene_seq.reverse_complement()
    
    if gene_name:
        header = f"{locus_tag} {gene_name}"
    else:
        header = locus_tag
    
    description = "" if pd.isna(gene_name) else gene_name
    record = SeqRecord(gene_seq, id=locus_tag, description=description)
    output_records.append(record)

SeqIO.write(output_records, fasta_output, 'fasta')
