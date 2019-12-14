#!/usr/bin/env python
import sys
import yaml

import Command
from Task import Task
from Switch import Switch
from Variables import Variables
from Result import Result

with open(sys.argv[2]) as f:
    yml = yaml.load(f, Loader=yaml.SafeLoader)
with open('/Users/hirano.shigetoshi/fzfyml_list.txt', 'a') as f:
    f.write(sys.argv[2] + '\n')
variables = Variables(sys.argv)
switch = Switch(yml.get('switch_task', {}), variables)
base_task = Task(yml['base_task'], variables, switch.get_expect())
task = base_task

if sys.argv[1] == 'run':
    while True:
        r = Command.execute(task.get_cmd())
        result = Result(r, task.get_transform())
        if result.is_empty():
            break
        if switch.has(result.key):
            variables.set_pre_result(result)
            task = task.create_switch_task(switch.get_switch_dict(result.key))
        else:
            task.output(result)
            break
elif sys.argv[1] == 'debug':
    if len(sys.argv) > 3:
        next_task = switch.get(sys.argv[-1])
        task = task.create_switch_task(next_task)
    print(task.get_cmd())
else:
    raise ValueError("")
