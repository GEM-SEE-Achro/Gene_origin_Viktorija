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
        fasta = config["input"]
    output:
        hits = "results/eggnog/eggnog.emapper.hits",
        seed = "results/eggnog/eggnog.emapper.seed_orthologs",
        annotation = "results/eggnog/eggnog.emapper.annotations"
    params:
        eggnog_db = config["eggnog"]["db"],
        prefix = "results/eggnog/eggnog"
    conda:
        "../envs/eggnog.yaml"
    threads: 8
    shell:
        """
        emapper.py -i {input.fasta} -o {params.prefix} --data_dir {params.eggnog_db} \
            -m diamond --itype genome --cpu {threads} 
        """


