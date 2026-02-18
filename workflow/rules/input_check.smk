rule check_for_input:
    output:
        pass_flag = "results/pass_checks.done"
    params:
        input_type = config["input_type"],
        input_fasta = config["input"],
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
    shell:
        """
        python ./scripts/input_check.py {params.input_type} {params.input_fasta} {params.bakta_db_type} \
            {params.bakta_db_update} {params.bakta_db_threads} {params.abricate_mincov} \
            {params.abricate_minid} {params.abricate_threads} {params.eggnog_threads} \
            {params.metagraph_threads}

        touch {output.pass_flag}
        """