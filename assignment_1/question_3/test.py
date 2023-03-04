import os
import subprocess
import time

os.chdir(os.path.dirname(__file__))

for L in range(1, 9):
    subprocess.Popen(['python3', 'server.py'])
    time.sleep(1)
    subprocess.Popen(['python3', 'client.py', '--L', str(L)])
    time.sleep(5)
