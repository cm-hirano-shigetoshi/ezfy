import os, sys, yaml

base_opts = set()

def main(args):
  (template, yml) = (args[1], args[2])
  with open(template) as file:
    template = "".join(file.readlines())
  t = template
  #print(template)

  with open(yml) as file:
    settings = yaml.load(file)
  #print(settings)

  global base_opts
  if "opts" in settings["base_task"]:
    base_opts = set(settings["base_task"]["opts"])
  sub = {}

  sub["fzf"] = settings.get("fzf", "fzf")

  sub["base_task.input"] = settings["base_task"]["input"]
  sub["base_task.query"] = settings["base_task"].get("query", "")
  sub["base_task.preview"] = settings["base_task"].get("preview", "echo {}")
  sub["base_task.opts"]  = " ".join(["--"+x for x in base_opts])

  sub["binds"] = ""
  if "binds" in settings:
    sub["binds"] = get_binds(**settings["binds"])

  sub["expects.definition"] = "ctrl-m"
  sub["expects.operation"] = ""
  if "expects" in settings:
    for key, ope in settings["expects"].items():
      if key != "select-1":
        sub["expects.definition"] += "," + key
      if key == "enter":
        sub["expects.operation"] += "    } elsif ($k eq 'enter' || $k eq 'select-1') {\n"
      else:
        sub["expects.operation"] += "    } elsif ($k eq '" + key + "') {\n"
      if "stdout" in ope:
        if ope["stdout"] is None:
          sub["expects.operation"] += create_stdout(**{})
        else:
          sub["expects.operation"] += create_stdout(**ope["stdout"])
      if "pipe" in ope:
        sub["expects.operation"] += create_pipe(ope["pipe"])
      if "line_select" in ope:
        if ope["line_select"] is None:
          sub["expects.operation"] += create_line_select(**{})
        else:
          sub["expects.operation"] += create_line_select(**ope["line_select"])
      if "continue" in ope:
        sub["expects.operation"] += create_next_task(key, **ope["continue"])

  sub["base_task.line_select.filter"] = ""
  sub["extra.declaration"] = ""
  sub["extra.before_fzf"] = ""
  if "line_select" in settings["base_task"]:
    sub["base_task.line_select.filter"] = settings["base_task"]["line_select"].get("filter", "cat")
    sub["extra.declaration"] = "my $temp_file = `mktemp -t 'fzfer_line_select_XXXXXXXX'`;"
    sub["extra.before_fzf"] = "| tee '$temp_file' | $filter | cat -n";

  t = t.replace("${fzf}", sub["fzf"])
  t = t.replace("${base_task.input}", sub["base_task.input"])
  t = t.replace("${base_task.query}", sub["base_task.query"])
  t = t.replace("${base_task.preview}", sub["base_task.preview"])
  t = t.replace("${base_task.opts}", sub["base_task.opts"])
  t = t.replace("${base_task.line_select.filter}", sub["base_task.line_select.filter"])
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

def create_pipe(cmd):
  out = []
  out.append("        my $pipe = q| " + cmd + ";")
  out.append("        open(PIPE, $pipe);")
  out.append("        print PIPE join(\"\\n\", @{$ref_outputs});")
  out.append("        close(PIPE);")
  return "\n".join(out) + "\n"

def create_stdout(**opts):
  out = []
  if "nth" in opts:
    delimiter = opts.get("delimiter", "\\s+")
    out.append("        my $nth_delimiter = q" + delimiter + ";")
    out.append("        $ref_outputs = &nth($ref_outputs, \"" + str(opts["nth"]) + "\", \"$nth_delimiter\");")
  if "file" in opts:
    out.append("        $ref_outputs = &expand_home($ref_outputs);")
  if "quote" in opts:
    out.append("        my $quote = q" + opts["quote"] + ";")
    out.append("        $ref_outputs = &quotation($ref_outputs, $quote);")
  joiner = "\n"
  if "join" in opts:
    joiner = opts["join"] if opts["join"] is not None else " "
  out.append("        my $joiner = q" + joiner + ";")
  out.append("        my $prefix = q" + opts.get("prefix", "") + ";")
  out.append("        my $suffix = q" + opts.get("suffix", "") + ";")
  out.append("        print $prefix . join(\"\\n\", @{$ref_outputs}) . $suffix;")
  return "\n".join(out) + "\n"

def create_line_select(**opts):
  out = "        $ref_outputs = &line_select($temp_file, $ref_outputs);"
  return out + "\n" + create_stdout(**opts)

def create_next_task(key, **props):
  out = []
  out.append("        $query = qq" + expand_result(props.get("query", "${result:query}")) + ";")
  if "input" in props:
    out.append("        $input = q" + expand_result(props["input"]) + ";")
  if "preview" in props:
    out.append("        $preview = q" + expand_result(props["preview"]) + ";")

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

def expand_result(s):
  s = s.replace("${result:query}", "$q")
  s = s.replace("${result:key}", "$k")
  return s

if __name__ == "__main__":
  main(sys.argv)

