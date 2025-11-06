rule abricate:
    input:
        fasta = config["fasta_file"]
    output:
        tab = "results/abricate/abricate_results.tab"
    log:
        "Logs/abricate.log"
    conda:
        "../envs/abricate.yaml"
    shell:
        """
        abricate --mincov 50 --minid 80 {input.fasta} > {output.tab}
        """
    