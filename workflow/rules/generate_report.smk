rule generate_report:
    input:
        bakta_tsv = "results/bakta/bakta.tsv",
        bakta_txt = "results/bakta/bakta.txt",
        eggnog_annotations = "results/eggnog/eggnog.emapper.annotations",
        eggnog_orthologs = "results/eggnog/eggnog.emapper.seed_orthologs",
        abricate_summary = "results/abricate/abricate_summary.tab",
        abricate_ncbi = "results/abricate/abricate_AMRFinderPlus.tab",
        abricate_card = "results/abricate/abricate_CARD.tab",
        abricate_resfinder = "results/abricate/abricate_Resfinder.tab",
        metagraph = "results/metagraph/metagraph_matches.json"
    output:
        "results/reports/report.html"
    params:
        abricate_mincov = config["abricate"]["mincov"],
        abricate_minid = config["abricate"]["minid"]
    conda:
        "../envs/r_report.yaml"
    script:
        "../scripts/report.Rmd"