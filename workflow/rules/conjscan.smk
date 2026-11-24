rule conjscan_db:
    output:
        directory(config["conjscan"]["db"])
    conda:
        "../envs/conjscan.yaml"
    shell:
        """
        macsydata install -t {output} CONJScan
        """

rule conjscan:
    input:
        faa = "results/{sample}/bakta/bakta.faa",
        db = config["conjscan"]["db"]
    output:
        best = "results/{sample}/conjscan/{modelset}/best_solution.tsv"
    wildcard_constraints:
        modelset = "Chromosome|Plasmids"
    params:
        outdir = "results/{sample}/conjscan/{modelset}"
    threads:
         config["conjscan"]["threads"]
    conda:
        "../envs/conjscan.yaml"
    shell:
        """
        macsyfinder --db-type ordered_replicon \
            --sequence-db {input.faa} --models CONJScan/{wildcards.modelset} all \
            --models-dir {input.db} -w {threads} -o {params.outdir}
        """
