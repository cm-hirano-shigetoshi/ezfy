import sys
from Task import Task
import subprocess
from subprocess import PIPE

base_task = Task(sys.argv[1])

proc = subprocess.run(base_task.get_task(), shell=True, stdout=PIPE)
print(proc.stdout.decode('utf8'))
