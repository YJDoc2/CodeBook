from enum import Enum

class Lang_type(Enum):
    COMPILED = 0
    INTERPRETED =1

def get_lang_dict(*data):
    return {'ext':data[0],'compiler':data[1],'ops':data[2],'type':data[3]}

langs = {
    'C':get_lang_dict('.c','gcc','-o',Lang_type.COMPILED),
    'C++':get_lang_dict('.cpp','g++','-o',Lang_type.COMPILED),
    'C++14':get_lang_dict('.cpp','g++','-std=c++14 -o',Lang_type.COMPILED),
    'Java':get_lang_dict('.java','javac','',Lang_type.COMPILED),
    'Node':get_lang_dict('.js','node','',Lang_type.INTERPRETED),
    'Python 2':get_lang_dict('.py','python2','',Lang_type.INTERPRETED),
    'Python 3':get_lang_dict('.py','python3','',Lang_type.INTERPRETED),

}