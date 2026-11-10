rule bakta_db:
    output:
        db = os.path.join(config["bakta"]["db"],
            "db-light" if config["bakta"]["type"] == "light" else "db",
            "bakta.db")
    params:
        bakta_db = config["bakta"]["db"],
        db_type = config["bakta"]["type"]
    conda:
        "../envs/bakta.yaml"
    shell:
        """
        bakta_db download --output {params.bakta_db} --type {params.db_type}
        """

rule bakta_db_update:
    input:
        db = os.path.join(config["bakta"]["db"],
            "db-light" if config["bakta"]["type"] == "light" else "db",
            "bakta.db")
    output: 
        flag_done = temp("database_update.done"),
    params:
        bakta_db = os.path.join(config["bakta"]["db"],
            "db-light" if config["bakta"]["type"] == "light" else "db")
    conda: "../envs/bakta.yaml"
    shell:
        """
        bakta_db update --db {params.bakta_db} 
        touch {output.flag_done}
        """

rule bakta:
    input:
        bakta_db = os.path.join(config["bakta"]["db"],
            "db-light" if config["bakta"]["type"] == "light" else "db",
            "bakta.db"),
        fasta = lambda wc: SAMPLES[wc.sample],
        update_flag = "database_update.done" if config["bakta"]["update"] else [],
        check_flag = "results/{sample}/pass_checks.done"
    output:
        dir = directory("results/{sample}/bakta"),
        gff = "results/{sample}/bakta/bakta.gff3",
        faa = "results/{sample}/bakta/bakta.faa",
        fna = "results/{sample}/bakta/bakta.fna",
        tsv = "results/{sample}/bakta/bakta.tsv",
        txt = "results/{sample}/bakta/bakta.txt"
    threads:
        config["bakta"]["threads"]
    log:
        "Logs/{sample}/bakta.log"
    conda:
        "../envs/bakta.yaml"
    params:
        db = os.path.join(config["bakta"]["db"],
            "db-light" if config["bakta"]["type"] == "light" else "db"),
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