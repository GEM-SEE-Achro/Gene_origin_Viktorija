rule check_for_input:
    output:
        pass_flag = "results/{sample}/pass_checks.done"
    params:
        input_type = config["input_type"],
        input_fasta = lambda wc: SAMPLES[wc.sample],
        bakta_db_type = config["bakta"]["type"],
        bakta_db_update = config["bakta"]["update"],
        bakta_db_threads = config["bakta"]["threads"],
        abricate_mincov = config["abricate"]["mincov"],
        abricate_minid = config["abricate"]["minid"],
        abricate_threads = config["abricate"]["threads"],
        eggnog_threads = config["eggnog"]["threads"],
        metagraph_threads = config["metagraph"]["threads"]
    conda:
        "../envs/py.yaml"
    script:
        "../scripts/input_check.py"