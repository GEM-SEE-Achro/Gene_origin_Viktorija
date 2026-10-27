rule extract_genes:
    input:
        bakta_tsv = "results/{sample}/bakta/bakta.tsv",
        eggnog_tsv = "results/{sample}/eggnog/eggnog.emapper.annotations",
        abricate_amr_tab = "results/{sample}/abricate/abricate_AMRFinderPlus.tab",
        abricate_card_tab = "results/{sample}/abricate/abricate_CARD.tab",
        abricate_resfinder_tab = "results/{sample}/abricate/abricate_Resfinder.tab",
        abricate_plasmid_tab = "results/{sample}/abricate/abricate_PlasmidFinder.tab",
        genomad_plasmid_tsv = "results/{sample}/genomad/{sample}_summary/{sample}_plasmid_genes.tsv",
        genomad_virus_tsv = "results/{sample}/genomad/{sample}_summary/{sample}_virus_genes.tsv",
        bakta_fna = "results/{sample}/bakta/bakta.fna"
    output:
        output_fasta = "results/{sample}/metagraph/extracted_genes.fasta",
        selected_genes = "results/{sample}/metagraph/selected_genes.tsv",
        not_found = "results/{sample}/metagraph/not_found.txt"
    params:
        groups = config["metagraph"]["select"]["groups"],
        genes = config["metagraph"]["select"]["genes"],
        regions = lambda wc: config["metagraph"]["select"]["regions"].get(wc.sample, [])

    conda:
        "../envs/py.yaml"
    script:
        "../scripts/extract_genes_for_metagraph.py"

rule run_metagraph:
    input:
        cogv = "results/{sample}/metagraph/extracted_genes.fasta"
    output:
        res = "results/{sample}/metagraph/metagraph_matches.json"
    threads:
        config["metagraph"]["threads"]
    # Queries the public MetaGraph server; run.sh sets --resources metagraph_api=1
    # so samples query it one at a time instead of all at once.
    resources:
        metagraph_api = 1
    params:
        discovery_threshold = config["metagraph"]["discovery_threshold"],
        min_exact_match = config["metagraph"]["min_exact_match"],
        node_labels = config["metagraph"]["node_labels"]
    conda:
        "../envs/py.yaml"
    benchmark:
        "benchmarks/{sample}/run_metagraph.tsv"
    script:
        "../scripts/run_metagraph.py"