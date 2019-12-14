#!/usr/bin/env python
import sys
import yaml

import Command
from Task import Task
from Switch import Switch
from Variables import Variables

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
        result = Command.execute(task.get_cmd())
        if len(result) > 0:
            if not task.is_switch(result):
                task.output(result)
                break
            else:
                task.set_pre(result)
                next_task = switch.get(result.split('\n')[1])
                task = task.create_switch_task(next_task)
        else:
            break
elif sys.argv[1] == 'debug':
    if len(sys.argv) > 3:
        next_task = switch.get(sys.argv[-1])
        task = task.create_switch_task(next_task)
    print(task.get_cmd())
else:
    raise ValueError("")
