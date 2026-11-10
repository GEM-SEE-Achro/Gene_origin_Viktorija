ABRICATE_DBS = {
    "AMRFinderPlus" : "ncbi",
    "CARD" : "card",
    "Resfinder" : "resfinder",
    "PlasmidFinder" : "plasmidfinder"
}

wildcard_constraints:
    db = "|".join(ABRICATE_DBS.keys())

rule abricate:
    input:
        fna = "results/{sample}/bakta/bakta.fna",
        check_flag = "results/{sample}/pass_checks.done"
    output:
        tab = "results/{sample}/abricate/abricate_{db}.tab"
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
        abricate --db {params.db} --mincov {params.mincov} --minid {params.minid} {input.fna} > {output.tab}
        """

rule abricate_summary:
    input:
        tabs = expand("results/{{sample}}/abricate/abricate_{db}.tab", db=ABRICATE_DBS.keys())
    output:
        summary = "results/{sample}/abricate/abricate_summary.tab"
    log:
        "Logs/{sample}/abricate.log"
    conda:
        "../envs/abricate.yaml"
    shell:
        """
        abricate --summary {input.tabs} > {output.summary}
        """