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
        genomad_threads = config["genomad"]["threads"],
        metagraph_run = config["metagraph"]["run"],
        metagraph_threads = config["metagraph"]["threads"],
        metagraph_discovery_threshold = config["metagraph"]["discovery_threshold"],
        metagraph_min_exact_match = config["metagraph"]["min_exact_match"],
        metagraph_node_labels = config["metagraph"]["node_labels"],
        select_groups = config["metagraph"]["select"]["groups"],
        select_genes = config["metagraph"]["select"]["genes"],
        select_regions = config["metagraph"]["select"]["regions"],
        sample_names = list(SAMPLES.keys())
    conda:
        "../envs/py.yaml"
    script:
        "../scripts/input_check.py"