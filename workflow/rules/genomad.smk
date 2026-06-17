genomad_basename = os.path.splitext(os.path.basename(config["input"]))[0]

rule genomad_db:
    output:
        directory(config["genomad"]["db"])
    conda:
        "../envs/genomad.yaml"
    shell:
        """
        genomad download-database $(dirname {output})
        """

rule genomad:
    input:
        fna = "results/bakta/bakta.fna",
        db = config["genomad"]["db"],
        check_flag = "results/pass_checks.done"
    output:
        virus_summary = f"results/genomad/{genomad_basename}_summary/{genomad_basename}_virus_summary.tsv",
        virus_genes = f"results/genomad/{genomad_basename}_summary/{genomad_basename}_virus_genes.tsv",
        plasmid_summary = f"results/genomad/{genomad_basename}_summary/{genomad_basename}_plasmid_summary.tsv",
        plasmid_genes = f"results/genomad/{genomad_basename}_summary/{genomad_basename}_plasmid_genes.tsv"
    params:
        outdir = "results/genomad",
        renamed = f"results/genomad/{genomad_basename}.fna"
    threads:
        config["genomad"]["threads"]
    conda:
        "../envs/genomad.yaml"
    shell:
        """
        cp {input.fna} {params.renamed}
        genomad end-to-end --cleanup --threads {threads} {params.renamed} {params.outdir} {input.db}
        rm -f {params.renamed}
        """
