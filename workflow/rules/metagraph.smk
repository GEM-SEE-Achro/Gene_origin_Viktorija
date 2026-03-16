rule extract_cog:
    input:
        bakta_tsv = "results/bakta/bakta.tsv",
        eggnog_tsv = "results/eggnog/eggnog.emapper.annotations",
        input_fasta = config["input"]
    output:
        output_fasta = "results/metagraph/extracted_cog.fasta"
    conda:
        "../envs/py.yaml"
    script:
        "../scripts/extract_COGV.py"

rule run_metagraph:
    input:
        cogv = "results/metagraph/extracted_cog.fasta"
    output:
        res = "results/metagraph/metagraph_matches.json"
    threads:
        config["metagraph"]["threads"]
    conda:
        "../envs/py.yaml"
    script:
        "../scripts/run_metagraph.py"