configfile: "../config/config.yaml"

rule bakta:
    input:
        fasta = config["input"]
    output:
        dir = directory("results/bakta"),
        gff = "results/bakta/bakta.gff3"
    threads:
        config["bakta"]["threads"]
    log:
        "Logs/bakta.log"
    conda:
        "../envs/bakta.yaml"
    params:
        db = config["bakta"]["db"],
        prefix = "bakta"
    shell:
        """
        bakta --db {params.db} \
            --prefix {params.prefix} \
            --output {output.dir} \
            --threads {threads} \
            --force \
            {input.fasta} 
        """

rule process_gff:
    input:
        gff = "results/bakta/bakta.gff3",
        script = os.path.join("scripts", "parse_gff.py")
    output:
        parsed = "results/parsed_gff.txt"
    log:
        "Logs/process_gff.log"
    conda:
        "../envs/py.yaml"
    shell:
        "python3 {input.script} {input.gff} {output.parsed}"