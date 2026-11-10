rule generate_report:
    input:
        bakta_tsv = "results/{sample}/bakta/bakta.tsv",
        bakta_txt = "results/{sample}/bakta/bakta.txt",
        eggnog_annotations = "results/{sample}/eggnog/eggnog.emapper.annotations",
        eggnog_orthologs = "results/{sample}/eggnog/eggnog.emapper.seed_orthologs",
        abricate_summary = "results/{sample}/abricate/abricate_summary.tab",
        abricate_ncbi = "results/{sample}/abricate/abricate_AMRFinderPlus.tab",
        abricate_card = "results/{sample}/abricate/abricate_CARD.tab",
        abricate_resfinder = "results/{sample}/abricate/abricate_Resfinder.tab",
        abricate_plasmidfinder = "results/{sample}/abricate/abricate_PlasmidFinder.tab",
        genomad_virus = "results/{sample}/genomad/{sample}_summary/{sample}_virus_summary.tsv",
        genomad_plasmid = "results/{sample}/genomad/{sample}_summary/{sample}_plasmid_summary.tsv",
        metagraph = "results/{sample}/metagraph/metagraph_matches.json" if config["metagraph"]["run"] else [],
        selected_genes = "results/{sample}/metagraph/selected_genes.tsv" if config["metagraph"]["run"] else [],
        not_found = "results/{sample}/metagraph/not_found.txt" if config["metagraph"]["run"] else []
    output:
        "results/{sample}/report.html"
    params:
        sample = "{sample}",
        run_metagraph = config["metagraph"]["run"],
        abricate_mincov = config["abricate"]["mincov"],
        abricate_minid = config["abricate"]["minid"],
        groups = config["metagraph"]["select"]["groups"],
        genes = config["metagraph"]["select"]["genes"],
        regions = lambda wc: config["metagraph"]["select"]["regions"].get(wc.sample, [])
    conda:
        "../envs/r_report.yaml"
    script:
        "../scripts/report.Rmd"