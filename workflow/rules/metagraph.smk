rule extract_cog:
    input:
        bakta_tsv = "results/bakta/bakta.tsv",
        eggnog_tsv = "results/eggnog/eggnog.emapper.annotations",
        input_fasta = config["input"]
    output:
        output_fasta = "results/metagraph/extracted_cog.fasta"
    conda:
        "../envs/py.yaml"
    shell:
        """
        ./scripts/extract_COGV.py {input.bakta_tsv} {input.eggnog_tsv} {input.input_fasta} {output.output_fasta}
        """