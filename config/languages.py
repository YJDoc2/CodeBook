from enum import Enum


class Lang_type(Enum):
    COMPILED = 0
    INTERPRETED = 1


class C:
    lang_name = 'C'
    ext = '.c'
    compiler = 'gcc'
    ops = '-o'
    type = Lang_type.COMPILED
    compile_time = 5
    run_time = 5
    invalid = ["fopen", "fscan", "fgetc", "fprintf",
               "fputs", "fseek", "rewind", "fclose", "exec", "open", "openfd"]

    @staticmethod
    def get_compile_profile(id):
        output = C.ops+'./temp/'+id+'/a.out'
        return [C.compiler, './temp/'+id+'/code'+C.ext, output]

    @staticmethod
    def get_run_profile(id):
        return ['./a.out']


class CPP:

    lang_name = 'C++'
    ext = '.cpp'
    compiler = 'g++'
    ops = '-o'
    type = Lang_type.COMPILED
    compile_time = 5
    run_time = 5
    invalid = ["ofstream", "ifstream", "fstream"]

    @staticmethod
    def get_compile_profile(id):
        output = CPP.ops+'./temp/'+id+'/a.out'
        return [CPP.compiler, './temp/'+id+'/code'+CPP.ext, output]

    @staticmethod
    def get_run_profile(id):
        return ['./a.out']


class CPP14:

    lang_name = 'C++'
    ext = '.cpp'
    compiler = 'g++'
    ops = ' -o '
    type = Lang_type.COMPILED
    compile_time = 5
    run_time = 5
    invalid = ["ofstream", "ifstream", "fstream"]

    @staticmethod
    def get_compile_profile(id):
        output = CPP14.ops+'./temp/'+id+'/a.out'
        return [CPP14.compiler, './temp/'+id+'/code'+CPP14.ext, output]

    @staticmethod
    def get_run_profile(id):
        return ['./a.out']


class JAVA:

    lang_name = 'Java'
    ext = '.java'
    compiler = 'javac'
    ops = ''
    type = Lang_type.COMPILED
    compile_time = 5
    run_time = 5
    invalid = ["write", "close"]

    @staticmethod
    def get_compile_profile(id):
        return [JAVA.compiler, './temp/'+id+'/code'+JAVA.ext]

    @staticmethod
    def get_run_profile(id):
        return ['java', 'Main']


class NODE:

    lang_name = 'Node'
    ext = '.js'
    compiler = 'node'
    ops = ''
    type = Lang_type.INTERPRETED
    compile_time = 5
    run_time = 5
    invalid = ['document.write']
    @staticmethod
    def get_compile_profile(id):
        output = NODE.ops+'./temp/'+id+'/a.out'
        return [NODE.compiler, './temp/'+id+'/code'+NODE.ext, output]

    @staticmethod
    def get_run_profile(id):
        raise LookupError()


class PYTHON2:

    lang_name = 'Python 2'
    ext = '.py'
    compiler = 'python2'
    ops = ''
    type = Lang_type.INTERPRETED
    invalid = ["open"]
    compile_time = 5
    run_time = 5
    @staticmethod
    def get_compile_profile(id):
        output = PYTHON2.ops+'./temp/'+id+'/a.out'
        return [PYTHON2.compiler, './temp/'+id+'/code'+PYTHON2.ext, output]

    @staticmethod
    def get_run_profile(id):
        raise LookupError()


class PYTHON3:

    lang_name = 'Python 3'
    ext = '.py'
    compiler = 'python3'
    ops = ''
    type = Lang_type.INTERPRETED
    invalid = ["open"]
    compile_time = 5
    run_time = 5
    @staticmethod
    def get_compile_profile(id):
        output = PYTHON3.ops+'./temp/'+id+'/a.out'
        return [PYTHON3.compiler, './temp/'+id+'/code'+PYTHON3.ext, output]

    @staticmethod
    def get_run_profile(id):
        raise LookupError()
