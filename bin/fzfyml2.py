import re
import sys
import yaml
from Task import Task
from Continue import Continue
import subprocess
from subprocess import PIPE

with open(sys.argv[2]) as f:
    yml = yaml.load(f, Loader=yaml.SafeLoader)
next_tasks = Continue(yml.get('continue', {}))
base_task = Task(yml['base_task'], next_tasks.get_expect())

if sys.argv[1] == 'run':
    proc = subprocess.run(base_task.get_cmd(), shell=True, stdout=PIPE)
    result = proc.stdout.decode('utf8')
    if True:
        base_task.stdout(result)
    else:
        key = Task.get_continue_key(result)
        new_task = base_task.create_continue_task(next_tasks, key)
        proc = subprocess.run(new_task.get_cmd(), shell=True, stdout=PIPE)
        result = proc.stdout.decode('utf8')
elif sys.argv[1] == 'debug':
    print(base_task.get_cmd())
else:
    raise ValueError("")

