ABRICATE_DBS = {
    "AMRFinderPlus" : "ncbi",
    "CARD" : "card",
    "Resfinder" : "resfinder",
    "PlasmidFinder" : "plasmidfinder"
}

rule abricate:
    input:
        fasta = config["input"],
        check_flag = "results/pass_checks.done"
    output:
        tab = "results/abricate/abricate_{db}.tab"
    threads:
        config["abricate"]["threads"]
    conda:
        "../envs/abricate.yaml"
    params:
        db = lambda wc: ABRICATE_DBS[wc.db],
        mincov = config["abricate"]["mincov"],
        minid = config["abricate"]["minid"]
    shell:
        """
        abricate --db {params.db} --mincov {params.mincov} --minid {params.minid} {input.fasta} > {output.tab}
        """

rule abricate_summary:
    input:
        tabs = expand("results/abricate/abricate_{db}.tab", db=ABRICATE_DBS.keys())
    output:
        summary = "results/abricate/abricate_summary.tab"
    log:
        "Logs/abricate.log"
    conda:
        "../envs/abricate.yaml"
    shell:
        """
        abricate --summary {input.tabs} > {output.summary}
        """