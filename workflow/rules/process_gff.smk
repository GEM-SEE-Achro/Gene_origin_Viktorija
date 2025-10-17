rule process_gff:
    input:
        gff = config["gff_file"],
        script = os.path.join("scripts", "parse_gff.py")
    output:
        parsed = "results/parsed_gff.txt"
    log:
        "Logs/process_gff.log"
    conda:
        "../envs/py.yaml"
    shell:
        "python3 {input.script} {input.gff} {output.parsed}"