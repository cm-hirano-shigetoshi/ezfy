import re
import sys
from Task import Task
import subprocess
from subprocess import PIPE

if sys.argv[1] == 'run':
    base_task = Task(sys.argv[2])
    proc = subprocess.run(base_task.get_cmd(), shell=True, stdout=PIPE)
    print(re.sub('\n$', '', proc.stdout.decode('utf8')))
elif sys.argv[1] == 'debug':
    base_task = Task(sys.argv[2])
    print(base_task.get_cmd())
else:
    raise ValueError("")

