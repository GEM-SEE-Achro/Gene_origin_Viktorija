rule generate_report:
    input:
        bakta_tsv = "results/bakta/bakta.tsv",
        bakta_txt = "results/bakta/bakta.txt",
        eggnog_annotations = "results/eggnog/eggnog.emapper.annotations",
        eggnog_orthologs = "results/eggnog/eggnog.emapper.seed_orthologs",
        abricate_summary = "results/abricate/abricate_summary.tab"
    output:
        "results/reports/report.html"
    conda:
        "../envs/r_report.yaml"
    script:
        "../scripts/report.Rmd"