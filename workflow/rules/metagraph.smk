genomad_basename = os.path.splitext(os.path.basename(config["input"]))[0]

rule extract_genes:
    input:
        bakta_tsv = "results/bakta/bakta.tsv",
        eggnog_tsv = "results/eggnog/eggnog.emapper.annotations",
        abricate_amr_tab = "results/abricate/abricate_AMRFinderPlus.tab",
        abricate_card_tab = "results/abricate/abricate_CARD.tab",
        abricate_resfinder_tab = "results/abricate/abricate_Resfinder.tab",
        abricate_plasmid_tab = "results/abricate/abricate_PlasmidFinder.tab",
        genomad_plasmid_tsv = f"results/genomad/{genomad_basename}_summary/{genomad_basename}_plasmid_genes.tsv",
        genomad_virus_tsv = f"results/genomad/{genomad_basename}_summary/{genomad_basename}_virus_genes.tsv",
        input_fasta = config["input"]
    output:
        output_fasta = "results/metagraph/extracted_genes.fasta"
    conda:
        "../envs/py.yaml"
    script:
        "../scripts/extract_genes_for_metagraph.py"

rule run_metagraph:
    input:
        cogv = "results/metagraph/extracted_genes.fasta"
    output:
        res = "results/metagraph/metagraph_matches.json"
    threads:
        config["metagraph"]["threads"]
    params:
        discovery_threshold = config["metagraph"]["discovery_threshold"],
        min_exact_match = config["metagraph"]["min_exact_match"],
        node_labels = config["metagraph"]["node_labels"]
    conda:
        "../envs/py.yaml"
    benchmark:
        "benchmarks/run_metagraph.tsv"
    script:
        "../scripts/run_metagraph.py"