#!/usr/bin/env python3
import sys
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

# All the input files
bakta_tsv = snakemake.input.bakta_tsv
eggnog_tsv = snakemake.input.eggnog_tsv
abricate_amr_tab = snakemake.input.abricate_amr_tab
abricate_card_tab = snakemake.input.abricate_card_tab
abricate_resfinder_tab = snakemake.input.abricate_resfinder_tab
abricate_plasmid_tab = snakemake.input.abricate_plasmid_tab
genomad_plasmid_tsv = snakemake.input.genomad_plasmid_tsv
genomad_virus_tsv = snakemake.input.genomad_virus_tsv
fasta_input = snakemake.input.input_fasta
fasta_output = snakemake.output.output_fasta

# Reading and parsing eggnog tsv file
with open(eggnog_tsv, 'r') as f:
    lines = f.readlines()

data_start_index = 0
for i, line in enumerate(lines):
    if line.startswith('#query'):
        data_start_index = i
        break

eggnog_df = pd.read_csv(eggnog_tsv, sep='\t', skiprows=data_start_index, header=0)
eggnog_mask = eggnog_df['COG_category'].str.contains('V', na=False) | \
              eggnog_df['COG_category'].str.contains('X', na=False)
cog_eggnog_id = set(eggnog_df[eggnog_mask]['#query'])

# Reading and parsing bakta tsv file
with open(bakta_tsv, 'r') as f:
    lines = f.readlines()

data_start_index = 0
for i, line in enumerate(lines):
    if line.startswith('#Sequence'):
        data_start_index = i
        break

bakta_df = pd.read_csv(bakta_tsv, sep='\t', skiprows=data_start_index, header=0)
# Drop features without a locus tag (e.g. oriC/oriV/oriT regions), they are not genes
bakta_df = bakta_df.dropna(subset=['Locus Tag'])
bakta_mask = bakta_df['DbXrefs'].str.contains('COG:V', na=False) | \
             bakta_df['DbXrefs'].str.contains('COG:X', na=False)
cog_bakta_id = set(bakta_df[bakta_mask]['Locus Tag'])

# Extracting COG=V and COG=X genes from both datasets
cog_all_id = cog_eggnog_id.union(cog_bakta_id)

# Finding bakta locus tags ovrlapping a region
def overlapping_locu_tags(seq_id, start, end):
    sub = bakta_df[bakta_df['#Sequence Id'] == seq_id]
    hits = sub[(sub['Start'] <= end) & (sub['Stop'] >= start)]
    return set(hits['Locus Tag'])

# Getting the contig name from a gene name in genomad
def genomad_contig(gene_name):
    s = str(gene_name)
    if '|' in s:
        return s.split('|')[0]
    return s.rsplit('_', 1)[0]

# Reading abricate tsv files and getting locus tags
abricate_id = set()
for tab in (abricate_amr_tab, abricate_card_tab, abricate_resfinder_tab, abricate_plasmid_tab):
    abr_df = pd.read_csv(tab, sep='\t')
    for _, row in abr_df.iterrows():
        abricate_id |= overlapping_locu_tags(row['SEQUENCE'], row['START'], row['END'])

# Reading genomad tsv files and getting locus tags
genomad_id = set()

plasmid_df = pd.read_csv(genomad_plasmid_tsv, sep='\t')
for _, row in plasmid_df.iterrows():
    contig = genomad_contig(row['gene'])
    genomad_id |= overlapping_locu_tags(contig, row['start'], row['end'])

virus_df = pd.read_csv(genomad_virus_tsv, sep='\t')
for _, row in virus_df.iterrows():
    contig = genomad_contig(row['gene'])
    genomad_id |= overlapping_locu_tags(contig, row['start'], row['end'])
    

# Combining all locus tags
all_id = cog_all_id | abricate_id | genomad_id
selected_genes = bakta_df[bakta_df['Locus Tag'].isin(all_id)]

input_sequence = SeqIO.read(fasta_input, 'fasta')
output_records = []

# Extracting sequences for the selected genes and writing to output fasta file
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
