#!/usr/bin/env python
import sys
import yaml
from Task import Task
from Switch import Switch
from Variables import Variables
import subprocess
from subprocess import PIPE

with open(sys.argv[2]) as f:
    yml = yaml.load(f, Loader=yaml.SafeLoader)
with open('/Users/hirano.shigetoshi/fzfyml_list.txt', 'a') as f:
    f.write(sys.argv[2] + '\n')
variables = Variables(sys.argv)
next_tasks = Switch(yml.get('switch_task', {}), variables)
base_task = Task(yml['base_task'], variables, next_tasks.get_expect())
task = base_task

if sys.argv[1] == 'run':
    while True:
        proc = subprocess.run(task.get_cmd(), shell=True, stdout=PIPE)
        result = proc.stdout.decode('utf8')
        if len(result) > 0:
            if not task.is_switch(result):
                task.output(result)
                break
            else:
                task.set_pre(result)
                next_task = next_tasks.get(result.split('\n')[1])
                task = base_task.create_switch_task(next_task)
        else:
            break
elif sys.argv[1] == 'debug':
    if len(sys.argv) > 3:
        next_task = next_tasks.get(sys.argv[-1])
        task = task.create_switch_task(next_task)
    print(task.get_cmd())
else:
    raise ValueError("")
