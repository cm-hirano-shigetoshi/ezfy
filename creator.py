import sys
import yaml

base_opts = set()


def main(args):
    (template, yml) = (args[1], args[2])
    with open(template) as file:
        template = "".join(file.readlines())
    t = template
    # print(template)

    with open(yml) as file:
        settings = yaml.load(file)
    # print(settings)

    global base_opts
    if "opts" in settings["base_task"]:
        base_opts = set(settings["base_task"]["opts"])
    sub = {}

    sub["fzf"] = settings.get("fzf", "fzf")

    sub["variables"] = ""
    if "variables" in settings:
        for var in settings["variables"]:
            init = ""
            if settings["variables"][var] is not None:
                init = settings["variables"][var]
            sub["variables"] += "$tmp = q" + init + ";\n"
            sub["variables"] += "($ENV{" + var + "} = `echo \"$tmp\"`) =~ s/\\n+$//;\n"

    sub["base_task.input"] = settings["base_task"]["input"]
    sub["base_task.query"] = settings["base_task"].get("query", "")
    sub["base_task.preview"] = settings["base_task"].get("preview", "echo {}")
    sub["base_task.opts"] = " ".join(["--" + x for x in base_opts])

    sub["binds"] = ""
    if "binds" in settings:
        sub["binds"] = get_binds(**settings["binds"])

    sub["expects.definition"] = "ctrl-m"
    sub["expects.operation"] = ""
    if "expects" in settings:
        for key, operations in settings["expects"].items():
            # key definition
            if key != "select-1":
                sub["expects.definition"] += "," + key
            if key == "enter":
                sub["expects.operation"] += "    } elsif ($k eq 'enter' || $k eq 'select-1') {\n"
            else:
                sub["expects.operation"] += "    } elsif ($k eq '" + key + "') {\n"

            # value definition
            if "line_select" in operations:
                sub["expects.operation"] += select_line_select()
            if "pipe" in operations:
                sub["expects.operation"] += create_pipe(operations["pipe"])
            if "stdout" in operations:
                sub["expects.operation"] += create_stdout(*operations["stdout"])
            if "pipe" in operations or "stdout" in operations:
                sub["expects.operation"] += create_print()
            if "continue" in operations:
                sub["expects.operation"] += create_next_task(
                    key, **operations["continue"])

    sub["base_task.line_select.filter"] = ""
    sub["extra.declaration"] = ""
    sub["extra.before_fzf"] = ""
    if "line_select" in settings["base_task"]:
        sub["base_task.line_select.filter"] = settings["base_task"][
            "line_select"].get("filter", "cat")
        sub["extra.declaration"] = "my $temp_file = `mktemp -t 'fzfer_line_select_XXXXXXXX'`;"
        sub["extra.before_fzf"] = "| tee '$temp_file' | $filter | cat -n"

    t = t.replace("${fzf}", sub["fzf"])
    t = t.replace("${variables}", sub["variables"])
    t = t.replace("${base_task.input}", sub["base_task.input"])
    t = t.replace("${base_task.query}", sub["base_task.query"])
    t = t.replace("${base_task.preview}", sub["base_task.preview"])
    t = t.replace("${base_task.opts}", sub["base_task.opts"])
    t = t.replace("${base_task.line_select.filter}",
                  sub["base_task.line_select.filter"])
    t = t.replace("${binds}", sub["binds"])
    t = t.replace("${expects.definition}", sub["expects.definition"])
    t = t.replace("${expects.operation}", sub["expects.operation"])
    t = t.replace("${extra.declaration}", sub["extra.declaration"])
    t = t.replace("${extra.before_fzf}", sub["extra.before_fzf"])

    print(t)


def get_binds(**binds):
    out = []
    for k, v in binds.items():
        out.append(k + ":" + v)
    return "--bind='" + ",".join(out) + "'"


def create_stdout(*opts):
    out = []
    delimiter = "\\s+"
    joiner = " "
    for opt in opts:
        if "delimiter" in opt:
            delimiter = opt["delimiter"]
        elif "nth" in opt:
            out.append("        my $nth_delimiter = q" + delimiter + ";")
            out.append("        $ref_outputs = &nth($ref_outputs, \"" +
                       str(opt["nth"]) + "\", \"$nth_delimiter\");")
        elif "file" in opt:
            out.append("        $ref_outputs = &filepath($ref_outputs);")
        elif "quote" in opt:
            out.append("        $ref_outputs = &quotation($ref_outputs, q" + opt["quote"] + ");")
        elif "prefix" in opt:
            out.append("        $tmp = q" + opt["prefix"] + ";")
            out.append("        ($tmp = `echo \"$tmp\"`) =~ s/\\n+$//;")
            out.append("        $ref_outputs = &put_prefix($ref_outputs, $tmp);")
        elif "suffix" in opt:
            out.append("        $tmp = q" + opt["prefix"] + ";")
            out.append("        ($tmp = `echo \"$tmp\"`) =~ s/\\n+$//;")
            out.append("        $ref_outputs = &put_suffix($ref_outputs, $tmp);")
        elif "join" in opt:
            if opt["join"] is not None:
                joiner = opt
            out.append("        $ref_outputs = &join_lines($ref_outputs, q" + joiner + ");")
    return "\n".join(out) + "\n"


def create_pipe(cmd):
    out = []
    out.append("        $pipe = q| " + cmd + ";")
    return "\n".join(out) + "\n"


def create_print():
    out = []
    out.append("        open(PIPE, $pipe);")
    out.append("        print PIPE join(\"\\n\", @{$ref_outputs});")
    out.append("        close(PIPE);")
    return "\n".join(out) + "\n"


def select_line_select():
    out = []
    out.append("        $ref_outputs = &line_select($temp_file, $ref_outputs);")
    return "\n".join(out) + "\n"


def create_next_task(key, **props):
    out = []
    out.append("        $query = q" + props.get("query", "${q}") + ";")
    out.append("        $query =~ s/\\${q}/$q/g;")
    out.append("        $query =~ s/\\${k}/$k/g;")
    out.append("        $query =~ s/\\${o}/$o/g;")
    for var in props.keys():
        if len(var) == 4 and var.startswith("var"):
            out.append("        $tmp = q" + props[var] + ";")
            out.append("        $tmp =~ s/\\${q}/$q/g;")
            out.append("        $tmp =~ s/\\${k}/$q/g;")
            out.append("        $tmp =~ s/\\${o}/$q/g;")
            out.append("        ($ENV{" + var + "} = `echo \"$tmp\"`) =~ s/\\n+$//;")
    if "input" in props:
        out.append("        $input = q" + props["input"] + ";")
        out.append("        $input =~ s/\\${q}/$q/g;")
        out.append("        $input =~ s/\\${k}/$k/g;")
        out.append("        $input =~ s/\\${o}/$o/g;")
    if "preview" in props:
        out.append("        $preview = q" + props["preview"] + ";")
        out.append("        $preview =~ s/\\${q}/$q/g;")
        out.append("        $preview =~ s/\\${k}/$k/g;")
        out.append("        $preview =~ s/\\${o}/$o/g;")

    if "opts-clear" in props:
        opts = set()
    else:
        opts = base_opts
    if "opts" in props:
        opts = opts.union(set(props["opts"]))
    if "opts-remove" in props:
        opts = opts.difference(set(props["opts-remove"]))
    out.append("        $opts = q--" + " --".join(opts) + ";")
    out.append("        next;")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    main(sys.argv)
