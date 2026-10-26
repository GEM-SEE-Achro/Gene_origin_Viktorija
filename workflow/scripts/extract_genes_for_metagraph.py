#!/usr/bin/env python3
import sys
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from collections import defaultdict

# All the input files
bakta_tsv = snakemake.input.bakta_tsv
eggnog_tsv = snakemake.input.eggnog_tsv
abricate_amr_tab = snakemake.input.abricate_amr_tab
abricate_card_tab = snakemake.input.abricate_card_tab
abricate_resfinder_tab = snakemake.input.abricate_resfinder_tab
abricate_plasmid_tab = snakemake.input.abricate_plasmid_tab
genomad_plasmid_tsv = snakemake.input.genomad_plasmid_tsv
genomad_virus_tsv = snakemake.input.genomad_virus_tsv
bakta_fna = snakemake.input.bakta_fna
fasta_output = snakemake.output.output_fasta
selected_genes_tsv = snakemake.output.selected_genes
not_found_txt = snakemake.output.not_found
gene_groups = snakemake.params.groups
genes = snakemake.params.genes
gene_regions = snakemake.params.regions

# Reading and parsing eggnog tsv file
with open(eggnog_tsv, 'r') as f:
    lines = f.readlines()

data_start_index = 0
for i, line in enumerate(lines):
    if line.startswith('#query'):
        data_start_index = i
        break

eggnog_df = pd.read_csv(eggnog_tsv, sep='\t', skiprows=data_start_index, header=0)

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

# Locus tag -> list of reasons why the gene was selected
reasons = defaultdict(list)

# Adding a reason to each of the given locus tags
def add(locus_tags, reason):
    for tag in locus_tags:
        if reason not in reasons[tag]:
            reasons[tag].append(reason)

# COG groups, e.g. "cog:VX": genes with COG V or X in Bakta (DbXrefs) or EggNOG (COG_category)
for group in gene_groups:
    if group.startswith("cog:"):
        for letter in group.split(":", 1)[1]:
            bakta_ids = set(bakta_df[bakta_df['DbXrefs'].str.contains(f'COG:{letter}', na=False)]['Locus Tag'])
            eggnog_ids = set(eggnog_df[eggnog_df['COG_category'].str.contains(letter, na=False)]['#query'])
            add(bakta_ids | eggnog_ids, f"cog:{letter}")

# Locus tags of genes overlapping the hits in one ABRicate file
def abricate_locus_tags(tab):
    ids = set()
    for _, row in pd.read_csv(tab, sep='\t').iterrows():
        ids |= overlapping_locu_tags(row['SEQUENCE'], row['START'], row['END'])
    return ids
if "amr" in gene_groups:
    for tab in (abricate_amr_tab, abricate_card_tab, abricate_resfinder_tab):
        add(abricate_locus_tags(tab), "amr")
if "plasmid" in gene_groups:
    add(abricate_locus_tags(abricate_plasmid_tab), "plasmid")

# Locus tags of genes inside the regions in one geNomad genes file
def genomad_locus_tags(tsv):
    ids = set()
    for _, row in pd.read_csv(tsv, sep='\t').iterrows():
        ids |= overlapping_locu_tags(genomad_contig(row['gene']), row['start'], row['end'])
    return ids
if "plasmid" in gene_groups:
    add(genomad_locus_tags(genomad_plasmid_tsv), "plasmid")
if "virus" in gene_groups:
    add(genomad_locus_tags(genomad_virus_tsv), "virus")    

# Requested genes or regions that were not found in this sample
not_found = []

# Gene names and locus tags in lower case, so matching is not case-sensitive.
gene_names = bakta_df['Gene'].fillna("").str.lower()
locus_tags = bakta_df['Locus Tag'].str.lower()

# Specific genes from the config: exact gene name or locus tag, or a prefix if the entry ends with *
for entry in genes:
    query = entry.lower()
    if query.endswith("*"):
        prefix = query[:-1]
        mask = gene_names.str.startswith(prefix) | locus_tags.str.startswith(prefix)
    else:
        mask = (gene_names == query) | (locus_tags == query)
    matched = set(bakta_df[mask]['Locus Tag'])
    if matched:
        add(matched, f"gene:{entry}")
    else:
        not_found.append(f"gene:{entry}")

# Regions from the config for this sample, e.g. "contig_1:10001-16122": all genes overlapping the region
for region in gene_regions:
    contig, coords = region.rsplit(":", 1)
    start, end = (int(x) for x in coords.split("-"))

    matched = overlapping_locu_tags(contig, start, end)
    if matched:
        add(matched, f"region:{region}")
    else:
        not_found.append(f"region:{region}")

# Selected genes: every gene with at least one reason
selected_genes = bakta_df[bakta_df['Locus Tag'].isin(list(reasons))]

# Contigs from Bakta's .fna, keyed by the same IDs as '#Sequence Id' in bakta.tsv (contig_1, contig_2, ...),
# so genomes with several contigs work too
contigs = SeqIO.to_dict(SeqIO.parse(bakta_fna, 'fasta'))
output_records = []

# Extracting sequences for the selected genes and writing to output fasta file
for _, gene in selected_genes.iterrows():
    start = gene['Start'] - 1
    end = gene['Stop']
    strand = gene['Strand']
    locus_tag = gene['Locus Tag']
    gene_name = gene['Gene']

    gene_seq = contigs[gene['#Sequence Id']].seq[start:end]

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

# Table of the selected genes and why each was selected, used in the report
selected_table = selected_genes[['Locus Tag', 'Gene', 'Product']].rename(
    columns={'Locus Tag': 'query', 'Gene': 'gene', 'Product': 'product'})
selected_table['selected_by'] = selected_table['query'].map(lambda tag: "; ".join(reasons[tag]))
selected_table.to_csv(selected_genes_tsv, sep='\t', index=False)

with open(not_found_txt, 'w') as f:
    f.write("".join(f"{entry}\n" for entry in not_found))