# Bicycle Transfiler

from sys import argv
from shlex import split
from re import sub

class BicycleIO:

    def Exception(self, message):
        print('오류:', message)
        exit()

    def __init__(self):
        self.run = False
        
        if 'python' in argv[0]:
            del argv[0]
        del argv[0]
        
        if argv:
            for i, arg in enumerate(argv):
                if arg.startswith('-'):
                    for subArg in arg[1:]:

                        # Argument Parser
                        if subArg == 'h':
                            print('\n'.join(['사용법: bicycle [파일명] [매개 변수...]',
                            '   -h: 도움말 출력',
                            '   -r: 컴파일 후 실행',
                            '   -o [파일명]: 출력 파일 설정']))
                            exit()
                        elif subArg == 'o':
                            self.output = argv.pop(i+1)
                        elif subArg == 'r':
                            self.run = True

                else:
                    if 'input' not in dir(self):
                        self.input = argv[i]   
        else:
            self.Exception('매개 변수가 없습니다. 매개 변수의 목록은 -h로 확인하실 수 있습니다.')

        if 'input' not in dir(self):
            self.Exception('입력 파일 매개 변수가 없습니다. 변환할 파일명을 입력해주세요.')
        if 'output' not in dir(self):
            self.output = 'out.py'

    def Read(self):
        try:
            return open(self.input, encoding = 'UTF-8').read()     
        except:
            self.Exception('입력 파일 매개 변수에 입력된 파일이 존재하지 않습니다.')

    def Write(self, code):
        try:
            open(self.output, 'w').write(code)
            if self.run:
                exec(open(self.output).read())
        except:
            self.Exception('출력에 실패했습니다.')

def Transfile(original):
    FUNC = {}
    CODE = ''
    for line in original.splitlines():

        nil = (len(line) - len(line.lstrip()))

        # Parsing
        cmd = split(line, posix = False)
        for idx, item in enumerate(cmd):
            if item[0] in ['\'', '"']:
                item = sub(r"(\\\()", "{", item)
                cmd[idx] = 'f' + sub(r"[\)]", "}", item)
            if item in list(FUNC.keys()):
                param = []
                for inner in cmd[idx + 1:]:
                    if inner.endswith(','):
                        param.append(inner[:-1])
                    else:
                        if param: param.append(inner)
                        break
                if len(param) == FUNC[item]:
                    for params in param:
                        for items in cmd:
                            if params in items: cmd.remove(items)
                    cmd[idx] = f'{item}({",".join(param)})'
                elif not param:
                    try:
                        exec(f'def a(t): print(t); a({cmd[idx + 1]})')
                        cmd[idx] = f'{item}({cmd.pop(idx + 1)})'
                    except:
                        cmd[idx] = f'{item}()'

        # Removing Exception
        if not cmd:
            out = line
            continue

        # Print Function
        if cmd[-1] in ['출력', '말하기']:
            out = f'print({" ".join(cmd[:-1])})'
        
        # Conditional
        elif cmd[0] in ['만약', '만약에', '아니고', '또는', '아니라면:', '아니면:']:

            if cmd[-1].endswith('라면:'):
                if cmd[-1][-4] == '이':
                    outTrim = 4
                elif cmd[-1][-5] + cmd[-1][-4] == '아니':
                    outTrim = 5
                else: outTrim = 3
                cmd[-1] = cmd[-1][:-outTrim] + ':'

            if cmd[0] in ['만약', '만약에']:
                out = f'if {" ".join(cmd[1:])}'

            elif cmd[0] in ['아니고', '또는']:
                out = f'elif {" ".join(cmd[1:])}'

            else: out = 'else:'

        # Function
        elif cmd[0][-1] + cmd[-1][-1] == '::':
            if len(cmd[1:]) == 0:
                FUNC[cmd[0][:-2]] = len(cmd[1:])
                out = f'def {cmd[0][:-2]}():'
            else:
                FUNC[cmd[0][:-1]] = len(cmd[1:])
                out = f'def {cmd[0][:-1]}({" ".join(cmd[1:])[:-1]}):'
        elif cmd[-1] in ['반환', '돌려주기']:
            out = f'return {" ".join(cmd[:-1])}'

        # For
        elif cmd[-1].endswith('까지:'):
            if cmd[-2].endswith('부터'):
                outRange = cmd[-2][:-2]
            else: outRange = 0
            out = f'for {cmd[0][:-1]} in range({outRange}, {cmd[-1][:-3]}):'
        
        elif cmd[-1].endswith('로부터:'):
            if cmd[-1][-5] == '으':
                outTrim = 5
            else: outTrim = 4
            out = f'for {cmd[0][:-1]} in {cmd[-1][:-outTrim]}:'

        elif cmd[-1] == '불러오기':
            mod = open(cmd[0] + '.byc', encoding = 'UTF-8').read()
            for item in mod.splitlines():
                if item.startswith('def'):
                    fnc = item[4:].split('(')
                    FUNC[fnc[0]] = len(fnc[1][0].split(')')[0].split(','))
            CODE = f'\n# Module {cmd[0]}\n{mod}\n# Module End\n{CODE}'
            continue

        else:
            CODE += f'\n{" ".join(cmd)}'
            continue

        CODE += f'\n{nil * " " + out}'
    
    return CODE

if __name__ == '__main__':
    IO = BicycleIO()
    CODE = Transfile(IO.Read())

    print('변환을 완료했습니다.\n')
    IO.Write('# Transfiled from Bicycle\n' + CODE)
