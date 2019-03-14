import sys, yaml

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
  base_opts = set(settings["base_task"]["opts"])
  sub = {}

  sub["fzf"] = settings["fzf"]

  sub["base_task.input"] = settings["base_task"]["input"]
  sub["base_task.query"] = settings["base_task"].get("query", "")
  sub["base_task.preview"] = settings["base_task"].get("preview", "echo {}")
  sub["base_task.opts"]  = "--" + " --".join(base_opts)

  sub["binds"] = "up:up"
  if "binds" in settings:
    sub["binds"] = get_binds(**settings["binds"])

  sub["expects.definition"] = "ctrl-m"
  sub["expects.operation"] = ""
  if "expects" in settings:
    for key, ope in settings["expects"].items():
      sub["expects.definition"] += "," + key
      sub["expects.operation"] += "    } elsif ($k eq '" + key + "') {\n"
      if "stdout" in ope:
        sub["expects.operation"] += create_stdout()
      if "pipe" in ope:
        sub["expects.operation"] += create_pipe(ope["pipe"])
      if "continue" in ope:
        sub["expects.operation"] += create_next_task(key, **ope["continue"])

  t = t.replace("${fzf}", sub["fzf"])
  t = t.replace("${base_task.input}", sub["base_task.input"])
  t = t.replace("${base_task.query}", sub["base_task.query"])
  t = t.replace("${base_task.preview}", sub["base_task.preview"])
  t = t.replace("${base_task.opts}", sub["base_task.opts"])
  t = t.replace("${binds}", sub["binds"])
  t = t.replace("${expects.definition}", sub["expects.definition"])
  t = t.replace("${expects.operation}", sub["expects.operation"])

  print(t)

def get_binds(**binds):
  out = []
  for k, v in binds.items():
    out.append(k + ":" + v)
  return ",".join(out)

def create_stdout():
  out = []
  out.append("        print &join_outputs($ref_outputs, \"\\n\", 0, \"\");")
  return "\n".join(out) + "\n"

def create_pipe(cmd):
  if cmd is None:
    cmd = "cat"
  out = []
  out.append("        open(my $stdout, '| " + cmd + "');")
  out.append("        print $stdout &join_outputs($ref_outputs, \"\\n\", 1, \"\");")
  out.append("        close($stdout);")
  return "\n".join(out) + "\n"

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
  out.append("        $opts = '--" + " --".join(opts) + "';")
  out.append("        next;")
  return "\n".join(out) + "\n"

def expand_result(s):
  s = s.replace("${result:query}", "$q")
  s = s.replace("${result:key}", "$k")
  return s

if __name__ == "__main__":
  main(sys.argv)

