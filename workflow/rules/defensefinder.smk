rule defensefinder_db:
    output:
        directory(config["defensefinder"]["db"])
    conda:
        "../envs/defensefinder.yaml"
    shell:
        """
        defense-finder update --models-dir {output}
        """

rule defensefinder:
    input:
        faa = "results/{sample}/bakta/bakta.faa",
        db = config["defensefinder"]["db"]
    output:
        systems = "results/{sample}/defensefinder/bakta_defense_finder_systems.tsv",
        genes = "results/{sample}/defensefinder/bakta_defense_finder_genes.tsv",
        hmmer = "results/{sample}/defensefinder/bakta_defense_finder_hmmer.tsv"
    params:
        outdir = "results/{sample}/defensefinder"
    threads:
        config["defensefinder"]["threads"]
    conda:
        "../envs/defensefinder.yaml"
    shell:
        """
        defense-finder run -o {params.outdir} --models-dir {input.db} -w {threads} \
            {input.faa}
        """