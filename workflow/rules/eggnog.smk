rule eggnog_db:
    output: 
        db = os.path.join(config["eggnog"]["db"], "eggnog.db"),
        dmnd = os.path.join(config["eggnog"]["db"], "eggnog_proteins.dmnd")
    params:
        eggnog_db = config["eggnog"]["db"]
    conda:
        "../envs/eggnog.yaml"
    threads: 1
    shell:
        """
        download_eggnog_data.py -y --data_dir {params.eggnog_db}
        """

rule eggnog_mapper:
    input:
        db = os.path.join(config["eggnog"]["db"], "eggnog.db"),
        dmnd = os.path.join(config["eggnog"]["db"], "eggnog_proteins.dmnd"),
        faa = "results/bakta/bakta.faa"
    output:
        hits = "results/eggnog/eggnog.emapper.hits",
        seed = "results/eggnog/eggnog.emapper.seed_orthologs",
        annotation = "results/eggnog/eggnog.emapper.annotations"
    threads:
        config["eggnog"]["threads"]
    params:
        eggnog_db = config["eggnog"]["db"],
        prefix = "results/eggnog/eggnog"
    conda:
        "../envs/eggnog.yaml"
    threads: 8
    shell:
        """
        emapper.py -i {input.faa} -o {params.prefix} --data_dir {params.eggnog_db} \
            -m diamond --itype proteins --cpu {threads}
        """


