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
        fasta = config["input"],
        db = config["genomad"]["db"],
        check_flag = "results/pass_checks.done"
    output:
        virus_summary = f"results/genomad/{genomad_basename}_summary/{genomad_basename}_virus_summary.tsv",
        plasmid_summary = f"results/genomad/{genomad_basename}_summary/{genomad_basename}_plasmid_summary.tsv"
    params:
        outdir = "results/genomad"
    threads:
        config["genomad"]["threads"]
    conda:
        "../envs/genomad.yaml"
    shell:
        """
        genomad end-to-end --cleanup --threads {threads} {input.fasta} {params.outdir} {input.db}
        """
