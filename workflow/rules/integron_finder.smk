rule integron_finder:
    input:
        fna = "results/{sample}/bakta/bakta.fna",
    output:
        sum= "results/{sample}/integron_finder/Results_Integron_Finder_bakta/bakta.summary"
    params:
        outdir =  "results/{sample}/integron_finder"
    threads:
        config["integron_finder"]["threads"]
    conda:
        "../envs/integron_finder.yaml"
    shell:
        """
        integron_finder --local-max --promoter-attI --cpu {threads} --outdir {params.outdir} {input.fna}
        """