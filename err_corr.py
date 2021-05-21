import functools as ft

def error_correction(command):
    if type(command) == tuple:
        return command

    # print('Error correction started!')
    oracle_std_dict = {
        'asterisk' : '*', 'character' : 'varchar2(25)', 
        'semicolon' : ';', 'percentage': '%', 
        (' comma', ' kama', ' Kama', ' and') : ',',
        'greater than' : '>', 'less than' : '<', 
        ('equals', 'equal') : '=', 
        ('greater than or equal to', '> or = to') : '>=',
        ('less than or equal to', '< or = to') : '<=', 
        'not equal to' : '<>', 'open bracket ' : '(', ' close bracket' : ')',
        ('single quote', 'single quote', 'single coat' ) : "'",
        ('double coat', 'double quote', 'double quotes') : '"', 
        ' underscore ' : '_', 'some (' : 'sum(', 'has' : 'as'
    }

    #basic correection
    for k, v in oracle_std_dict.items():
        if type(k) == tuple:
            for lv in k:
                command = command.replace(lv, v)
        else:
            command = command.replace(k, v)
    #
    
    #Case conversion
    temp_command = list(command.split())
    uc = temp_command.count('uppercase')    
    lc = temp_command.count('lowercase')    
    
    try:
        s = 0
        while uc != 0:
            i = temp_command.index('uppercase')
            for j in range(i + 1, len(temp_command)):
                if temp_command[j].isalpha():
                    if s == 0:
                        break
                    temp_command[j] = temp_command[j].upper()
                if temp_command[j] == '"' or temp_command[j] == "'":
                    if s == 0:
                        s = 1
                    else:
                        s = 0
            temp_command.pop(i)
            uc -= 1
        s = 0
        while lc != 0:
            i = temp_command.index('lowercase')
            for j in range(i + 1, len(temp_command)):
                if temp_command[j].isalpha():
                    if s == 0:
                        break
                    temp_command[j] = temp_command[j].lower()
                if temp_command[j] == '"' or temp_command[j] == "'":
                    if s == 0:
                        s = 1
                    else:
                        s = 0
            temp_command.pop(i)
            lc -= 1
    except Exception:
        pass

    command = ft.reduce(lambda a, b: a + ' ' + b, temp_command)
    del temp_command
    #

    #adding semicolon
    if command[len(command) - 1] != ';':
        command += ';'
    #

    #striping the extra space
    finds_quote = False

    for i in command:
        if i == '"' or i == "'":
            finds_quote = True
            break
    else:
        print(command)
        return command

    if finds_quote == True:
        command = strip_inside_quotes(command)
    #

    print(command)
    return command

def strip_inside_quotes(cmd):
    final_command = ''
    s = False
    for i, v in enumerate(cmd):
        if v == "'" or v == '"':
            if s == False:
                s = True
            else:
                s = False
        elif s == True and v.isspace() == True:
            if not (cmd[i - 1].isalpha() and cmd[i+1].isalpha()):
                continue
        final_command += v
    return final_command



if __name__ == '__main__':
    error_correction(input('Enter the command: '))