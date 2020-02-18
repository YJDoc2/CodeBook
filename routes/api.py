from flask import request,Response,Blueprint
from uuid import uuid4
import subprocess
import os

api = Blueprint('api',__name__)

def get_compiler(lang,id):
    
    if lang == 'C':
        return '.c','gcc','-o'+id
    elif lang == 'C++':
        return '.cpp','g++','-o'+id
    elif lang == 'C++14':
        return '.cpp','g++','--std=c++14 -o'+id
    elif lang == 'Node':
        return '.js','node',''
    elif lang == 'Python 2':
        return '.py','python2',''
    elif lang == 'Python 3':
        return '.py','python3',''
    else:
        return 'err','err','err'
    
def del_files(*files):
    for file in files:
        os.remove('./'+file)


@api.route('/api',methods=['POST'])
def handle():
    form = request.form.to_dict()
    id = str(uuid4())
    lang = form['lang']
    ext,compiler,ops = get_compiler(lang,id)

    if lang == 'C' or lang =='C++' or lang =='C++14':
        langtype = 'Compiled'
    else:
        langtype = 'Interprited'

    codefile = open(id+ext,mode='w+')
    codefile.write(form['code'])
    codefile.flush()
    codefile.close()

    ipfile = open(id+'i.txt','w+')
    ipfile.write(form['input'])
    ipfile.flush()
    ipfile.close()
    ipfile = open(id+'i.txt','r')

    try:
        proc = subprocess.run([compiler,id+ext,ops],stdin=ipfile,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True,timeout = 5)
        op = str(proc.stdout)+'\n'+str(proc.stderr)
        if 'error' in op or 'Error' in op:
            ipfile.close()
            del_files(id+ext,id+'i.txt')
            return Response('Error : '+op,mimetype='text/plain',status=400)

        if langtype == 'Compiled':
            proc = subprocess.run(['./'+id],stdin=ipfile,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True,timeout = 5)
            op = str(proc.stdout)+'\n'+str(proc.stderr)
            if 'error' in op or 'Error' in op:
                ipfile.close()
                del_files(id+ext,id+'i.txt',id)
                return Response('Error : '+op,mimetype='text/plain',status=400)
    except subprocess.TimeoutExpired:
        ipfile.close()
        del_files(id+ext,id+'i.txt')
        if langtype == 'Compiled':
            del_files(id)
        return Response('Error : Timeout Occured',mimetype='text/plain',status=400)
    
    ipfile.close()
    del_files(id+ext,id+'i.txt')
    if langtype == 'Compiled':
        del_files(id)
    return Response('Success : Output :\n'+op,mimetype='text/plain',status=200)