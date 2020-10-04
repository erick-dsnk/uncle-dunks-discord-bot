import subprocess

def search(text):
    command = f'youtube-dl ytsearch:"{text}" -g'
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True).stdout.split()
    
    return result[0]
