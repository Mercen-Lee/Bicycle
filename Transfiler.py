# Bicycle Transfiler

from sys import argv

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

IO = BicycleIO()
CODE = '# Transfiled from Bicycle'

#for line in IO.Read().splitlines():

IO.Write(CODE)
print('변환을 완료했습니다.')
