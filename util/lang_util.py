from config import lang_config
import os

def get_compile_profile(id,lang):
    lang_data = lang_config.langs[lang]
    output = lang_data['ops']
    if lang != 'Java':
        output = output+'./temp/'+id+'/a.out'
        return [lang_data['compiler'],'./temp/'+id+'/code'+lang_data['ext'],output]
    else:
        return [lang_data['compiler'],'./temp/'+id+'/code'+lang_data['ext']]


def get_run_profile(id,lang):
    if lang == 'Java':
        return ['java','Main']
    else:
        return ['./a.out']