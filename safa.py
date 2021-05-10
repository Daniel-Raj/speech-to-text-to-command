import subprocess
val = '''select * from emp;'''

process = subprocess.Popen('sqlplus -S scott/tiger', shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=None)
process.stdin.write(val.encode('utf-8')) #passing command
stdOutput,stdError = process.communicate()
print(stdOutput.decode('utf-8'))
process.stdin.close()
