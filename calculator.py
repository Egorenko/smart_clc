VARIABLES = {}  # словарь переменных, глобальный, потому что таков путь пока что


def exit_():
    print('Bye!')
    exit()


def help_():
    print('Это калькулятор. Доступные команды: +, -, *, / и ().')


def identifier(s: str) -> bool or str:
    """Функция для проверки корректности идентификатора"""
    idn = ''
    for i in s:
        if i not in '-+= ':
            idn += i
        else:
            break
    if all(65 <= ord(i) <= 122 for i in idn):
        return idn
    return False


def assignment(s: str) -> bool or str:
    """Функция для подготовки значения"""
    ass = ''
    s = s[::-1]
    for i in s:
        if i not in '= ':
            ass += i
        else:
            break
    if not ass:
        return False
    return ass[::-1]


def letters_assigment(ass: str) -> str or bool:
    """Функция для проверки корректности ввода буквенного значения"""
    if all(65 <= ord(i) <= 122 for i in ass):
        return ass
    return False


def exist_assigment(ass: str) -> str or bool:
    """Функция для проверки существования переменной"""
    if ass in VARIABLES:
        return ass
    return False


def add_variable(idn: str, ass: str) -> None:
    """Функция для добавления переменной"""
    global VARIABLES
    VARIABLES.update({idn: ass})


def count_eq(s: str):
    """Функция для проверки вхождений символа равно"""
    if s.count('=') <= 1:
        return True
    return False


def calculation(s):
    """Функция для рассчетов"""
    if s.count('(') != 0 and s.count(')') == 0 or s.count('(') == 0 and s.count(')') != 0:
        return 'Invalid expression'
    if s.find('**') != -1 or s.find('//') != -1:
        return 'Invalid expression'
    s = s.replace('(', ' ( ').replace(')', ' ) ')
    while '--' in s or '++' in s or '-+' in s or '+-' in s:
        s = s.replace('++', '+').replace('--', '+').replace('-+', '-').replace('+-', '-')
    in_ = [i for i in s.split()]
    stack_operations = []
    out_ = []
    for i in in_:
        if i.isdigit():
            out_.append(int(i))
        elif i.isalpha():
            if exist_assigment(i):
                out_.append(int(VARIABLES[i]))
            else:
                return 'Unknown variable'
        elif i in '*/':
            while stack_operations and stack_operations[0] in '*/':
                out_.append(stack_operations.pop(0))
            else:
                stack_operations.insert(0, i)
        elif i in '-+':
            while stack_operations and stack_operations[0] in '-+*/':
                out_.append(stack_operations.pop(0))
            else:
                stack_operations.insert(0, i)
        elif i == '(':
            stack_operations.insert(0, i)
        elif i == ')':
            while stack_operations[0] != '(':
                out_.append(stack_operations.pop(0))
            else:
                del stack_operations[0]
    out_.extend(stack_operations)
    operator_ = ''
    first_operand = 0
    second_operand = 0
    while len(out_) != 1:
        num = 0
        for i in out_:
            if type(i) == str:
                operator_ = i
                first_operand = out_[out_.index(i) - 2]
                second_operand = out_[out_.index(i) - 1]
                num = out_.index(i) - 2
                del out_[out_.index(i) - 2:out_.index(i) + 1]
                break
        if operator_ == '+':
            first_operand = first_operand + second_operand
            out_.insert(num, first_operand)
        if operator_ == '-':
            first_operand = first_operand - second_operand
            out_.insert(num, first_operand)
        if operator_ == '*':
            first_operand = first_operand * second_operand
            out_.insert(num, first_operand)
        if operator_ == '/':
            first_operand = first_operand // second_operand
            out_.insert(num, first_operand)
    return first_operand


while True:
    command = input().strip()
    if command != '':
        if command[0] == '/':
            if command[1:] not in ('help', 'exit'):
                print('Unknown command')
            elif command[1:] == 'help':
                help_()
            else:
                exit_()
        elif '=' in command:
            id_ = identifier(command)
            if not id_:
                print('Invalid identifier')
            else:
                if not count_eq(command):
                    print('Invalid assignment')
                else:
                    var = assignment(command)
                    if not var and var != 0:
                        print('Invalid assignment')
                    else:
                        if any(i.isalpha() for i in var):
                            var = letters_assigment(var)
                            if not var:
                                print('Invalid assignment')
                            else:
                                var = exist_assigment(var)
                                if not var:
                                    print('Unknown variable')
                                else:
                                    var = VARIABLES.get(var)
                                    add_variable(id_, var)
                        else:
                            add_variable(id_, var)
        elif '+' in command or '-' in command or '*' in command or '/' in command:
            if command[-1] in '-+':
                print('Invalid expression')
            else:
                print(calculation(command))
        elif ' ' not in command:
            if command.isdigit():
                print(command)
            else:
                var = exist_assigment(command)
                if not var:
                    print('Unknown variable')
                else:
                    print(VARIABLES[var])
        else:
            print('Invalid expression')
