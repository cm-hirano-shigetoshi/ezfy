import yaml

def main():
  with open("template.pl") as file:
    template = "".join(file.readlines())
  t = template
  #print(template)
  with open("test.yml") as file:
    settings = yaml.load(file)
  #print(settings)
  sub = {}

  sub["init_task.input"] = settings["init_task"]["input"]
  sub["init_task.query"] = settings["init_task"].get("query", "")
  sub["init_task.preview"] = settings["init_task"].get("preview", "echo {}")
  sub["init_task.opts"]  = "--" + " --".join(settings["init_task"]["opts"])

  sub["expects.definition"] = "ctrl-m"
  sub["expects.operation"] = ""
  for key, ope in settings["expects"].items():
    sub["expects.definition"] += "," + key
    sub["expects.operation"] += "} elsif ($k eq '" + key + "') {"
    if "stdout" in ope:
      sub["expects.operation"] += create_stdout(ope["stdout"])
    if "continue" in ope:
      sub["expects.operation"] += create_next_task(key, **ope["continue"])

  t = t.replace("${init_task.input}", sub["init_task.input"])
  t = t.replace("${init_task.query}", sub["init_task.query"])
  t = t.replace("${init_task.preview}", sub["init_task.preview"])
  t = t.replace("${init_task.opts}", sub["init_task.opts"])
  t = t.replace("${expects.definition}", sub["expects.definition"])
  t = t.replace("${expects.operation}", sub["expects.operation"])

  print(t)

def create_stdout(cmd):
  if cmd is None:
    cmd = "cat"
  out = []
  out.append("        open(my $stdout, '| " + cmd + "');")
  out.append("        print $stdout join(\"\\n\", @{$ref_outputs});")
  out.append("        close($stdout);")
  return "\n" + "\n".join(out)

def create_next_task(key, **props):
  out = []
  out.append("        $query = \"" + expand_result(props.get("query", "${result:query}")) + "\";")
  if "input" in props:
    out.append("        $input = \"" + expand_result(props["input"]) + "\";")
  if "preview" in props:
    out.append("        $preview = \"" + expand_result(props["preview"]) + "\";")
  out.append("        next;")
  return "\n" + "\n".join(out)

def expand_result(s):
   s = s.replace("${result:query}", "$q")
   s = s.replace("${result:key}", "$k")
   return s

if __name__ == "__main__":
  main()

