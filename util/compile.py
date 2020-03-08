from config.languages import Lang_type
from config.lang_config import langs
from uuid import uuid4
import subprocess
import os
import shutil

error_words = ['error', 'Error', 'exception', 'Exception']


def del_files(id):
    print('./temp/'+id)
    shutil.rmtree('./temp/'+id+'/')


def compile_and_run_code(lang, code, ip):
    id = str(uuid4())

    os.makedirs(name='./temp/'+id)

    codefile = open('./temp/'+id+'/'+'code'+lang.ext, mode='w+')
    codefile.write(code)
    codefile.flush()
    codefile.close()

    ipfile = open('./temp/'+id+'/ip.txt', 'w+')
    ipfile.write(ip)
    ipfile.flush()
    ipfile.close()
    ipfile = open('./temp/'+id+'/ip.txt', 'r')
    cwd = os.getcwd()
    try:
        profile = lang.get_compile_profile(id)
        proc = subprocess.run(profile, stdin=ipfile, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, universal_newlines=True, timeout=lang.compile_time)
        op = str(proc.stdout)+'\n'+str(proc.stderr)
        if any(c in op for c in error_words):
            ipfile.close()
            del_files(id)
            return {'success': False, 'err': 'Error : '+op, 'timeout': False}

        if lang.type == Lang_type.COMPILED:
            profile = lang.get_run_profile(id)
            os.chdir('./temp/'+id)
            proc = subprocess.run(profile, stdin=ipfile, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, universal_newlines=True, timeout=lang.run_time)
            os.chdir(cwd)
            op = str(proc.stdout)+'\n'+str(proc.stderr)

            if any(c in op for c in error_words):
                ipfile.close()
                del_files(id)
                return {'success': False, 'err': 'Error : '+op, 'timeout': False}

    except subprocess.TimeoutExpired:
        ipfile.close()
        os.chdir(cwd)
        del_files(id)
        return {'success': False, 'err': 'Error : Time Out Occured', 'timeout': True}

    ipfile.close()
    del_files(id)
    return {'success': True, 'output': op}
