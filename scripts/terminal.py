import subprocess

def launch_terminal(command):
    subprocess.call(['gnome-terminal', '--', 'bash', '-c', command])
