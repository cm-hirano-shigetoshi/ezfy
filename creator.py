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
  for key, expect in settings["expects"].items():
    sub["expects.definition"] += "," + key
    sub["expects.operation"] += hoge(key, **expect)

  t = t.replace("${init_task.input}", sub["init_task.input"])
  t = t.replace("${init_task.query}", sub["init_task.query"])
  t = t.replace("${init_task.preview}", sub["init_task.preview"])
  t = t.replace("${init_task.opts}", sub["init_task.opts"])
  t = t.replace("${expects.definition}", sub["expects.definition"])
  t = t.replace("${expects.operation}", sub["expects.operation"])

  print(t)

def hoge(key, **props):
  out = []
  out.append("} elsif ($k eq '" + key + "') {")
  if "input" in props:
    out.append("        $input = '" + props["input"] + "';")
  if "query" in props:
    out.append("        $query = '" + props["query"] + "';")
  if "preview" in props:
    out.append("        $preview = '" + props["preview"] + "';")
  if "continue" in props:
    out.append("        next;")
  return "\n".join(out)


if __name__ == "__main__":
  main()

