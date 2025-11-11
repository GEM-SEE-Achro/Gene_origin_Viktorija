from BCBio import GFF
import sys

gff_file = sys.argv[1]
counts_file = sys.argv[2]

gene_types_to_count = {"CDS", "tRNA", "rRNA", "ncRNA", "gene"}

gene_count = 0
with open(gff_file) as f:
    for rec in GFF.parse(f):
        for feature in rec.features:
                if feature.type in gene_types_to_count:
                    gene_count += 1

with open(counts_file, "w") as out_f:
    out_f.write(f"Total genes:\n{gene_count}\n")