rule abricate_AMRFinderPlus:
    input:
        fasta = config["input"],
        check_flag = "results/pass_checks.done"
    output:
        tab = "results/abricate/abricate_AMRFinderPlus.tab"
    threads:
        config["abricate"]["threads"]
    log:
        "Logs/abricate.log"
    conda:
        "../envs/abricate.yaml"
    params:
        mincov = config["abricate"]["mincov"],
        minid = config["abricate"]["minid"]
    shell:
        """
        abricate --db ncbi --mincov {params.mincov} --minid {params.minid} {input.fasta} > {output.tab}
        """

rule abricate_CARD:
    input:
        fasta = config["input"],
        check_flag = "results/pass_checks.done"
    output:
        tab = "results/abricate/abricate_CARD.tab"
    threads:
        config["abricate"]["threads"]
    log:
        "Logs/abricate.log"
    conda:
        "../envs/abricate.yaml"
    params:
        mincov = config["abricate"]["mincov"],
        minid = config["abricate"]["minid"]
    shell:
        """
        abricate --db card --mincov {params.mincov} --minid {params.minid} {input.fasta} > {output.tab}
        """

rule abricate_Resfinder:
    input:
        fasta = config["input"],
        check_flag = "results/pass_checks.done"
    output:
        tab = "results/abricate/abricate_Resfinder.tab"
    threads:
        config["abricate"]["threads"]
    log:
        "Logs/abricate.log"
    conda:
        "../envs/abricate.yaml"
    params:
        mincov = config["abricate"]["mincov"],
        minid = config["abricate"]["minid"]
    shell:
        """
        abricate --db resfinder --mincov {params.mincov} --minid {params.minid} {input.fasta} > {output.tab}
        """

rule abricate_summary:
    input:
        ncbi = "results/abricate/abricate_AMRFinderPlus.tab",
        card = "results/abricate/abricate_CARD.tab",
        resfinder = "results/abricate/abricate_Resfinder.tab"
    output:
        summary = "results/abricate/abricate_summary.tab"
    log:
        "Logs/abricate.log"
    conda:
        "../envs/abricate.yaml"
    shell:
        """
        abricate --summary \
        {input.ncbi} \
        {input.card} \
        {input.resfinder} > {output.summary}
        """