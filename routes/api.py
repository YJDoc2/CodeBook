from flask import request,Response,Blueprint,json
from config import lang_config
from util import lang_util
from uuid import uuid4
import subprocess
import os
import shutil

api = Blueprint('api',__name__)

error_words = ['error','Error','exception','Exception']
  
def del_files(id):
    shutil.rmtree('./temp/'+id)


@api.route('/api',methods=['POST'])
def handle():
    form = request.form.to_dict()
    try:
        tmp = form['lang']
    except:
        return Response(json.dumps({'res':'Form Not found'}),mimetype="application/json",status=400)
    id = str(uuid4())
    lang = form['lang']
    lang_data = lang_config.langs[lang]

    os.makedirs(name='./temp/'+id)

    codefile = open('./temp/'+id+'/'+'code'+lang_data['ext'],mode='w+')
    codefile.write(form['code'])
    codefile.flush()
    codefile.close()

    ipfile = open('./temp/'+id+'/ip.txt','w+')
    ipfile.write(form['input'])
    ipfile.flush()
    ipfile.close()
    ipfile = open('./temp/'+id+'/ip.txt','r')

    try:
        profile = lang_util.get_compile_profile(id,lang)
        proc = subprocess.run(profile,stdin=ipfile,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True,timeout = 5)
        op = str(proc.stdout)+'\n'+str(proc.stderr)
        if any(c in op for c in error_words):
            ipfile.close()
            del_files(id)
            return Response('Error : '+op,mimetype='text/plain',status=400)

        if lang_data['type'] == lang_config.Lang_type.COMPILED:
            profile = lang_util.get_run_profile(id,lang)
            cwd = os.getcwd()
            os.chdir('./temp/'+id)
            proc = subprocess.run(profile,stdin=ipfile,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True,timeout = 5)
            os.chdir(cwd)
            op = str(proc.stdout)+'\n'+str(proc.stderr)
            
            if any(c in op for c in error_words):
                ipfile.close()
                del_files(id)
                return Response('Error : '+op,mimetype='text/plain',status=400)

    except subprocess.TimeoutExpired:
        ipfile.close()
        del_files(id)
        if langtype == 'Compiled':
            del_files(id)
        return Response('Error : Timeout Occured',mimetype='text/plain',status=400)
    
    ipfile.close()
    del_files(id)
    return Response('Success : Output :\n'+op,mimetype='text/plain',status=200)