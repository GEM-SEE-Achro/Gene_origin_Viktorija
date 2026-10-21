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
        fna = "results/{sample}/bakta/bakta.fna",
        db = config["genomad"]["db"],
        check_flag = "results/{sample}/pass_checks.done"
    output:
        virus_summary = "results/{sample}/genomad/{sample}_summary/{sample}_virus_summary.tsv",
        virus_genes = "results/{sample}/genomad/{sample}_summary/{sample}_virus_genes.tsv",
        plasmid_summary = "results/{sample}/genomad/{sample}_summary/{sample}_plasmid_summary.tsv",
        plasmid_genes = "results/{sample}/genomad/{sample}_summary/{sample}_plasmid_genes.tsv"
    params:
        outdir = "results/{sample}/genomad",
        renamed = "results/{sample}/genomad/{sample}.fna"
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
