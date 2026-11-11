rule isescan:
    input:
        fna = "results/{sample}/bakta/bakta.fna"
    output:
        sum = "results/{sample}/isescan/bakta/bakta.fna.sum",
        tsv = "results/{sample}/isescan/bakta/bakta.fna.tsv"
    params:
        outdir = "results/{sample}/isescan"
    threads:
        config["isescan"]["threads"]
    conda:
        "../envs/isescan.yaml"
    shell:
        """
        isescan.py --seqfile {input.fna} --output {params.outdir} --nthread {threads}
        """
