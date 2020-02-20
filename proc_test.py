import subprocess
import io

f = open('test.c',mode='w+')
w = '#include<stdio.h>\r\nvoid main(){ \r\nwhile(1);\n\rprintf("Hello World!");}'

f.write(w)
f.flush()
try :
    process = subprocess.run(['gcc','test.c'],stdout=subprocess.PIPE)
    process = subprocess.run(['./a.out'],stdout=subprocess.PIPE,universal_newlines=True,timeout=2)
    print(process.stdout)
except subprocess.TimeoutExpired:
    print('TIMEOUT !!!')


