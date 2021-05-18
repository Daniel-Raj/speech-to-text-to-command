import eel, speech_recognition as sr, subprocess, cx_Oracle as cxo, functools as ft

eel.init('web')
username, password = '', ''

@eel.expose
def speech_translation(tostop):
    # print('Listener is Ready!')
    if tostop != True:
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration = 0.5)
                eel.listen()
                audio_data = r.listen(source, phrase_time_limit = 20)

            data = r.recognize_google(audio_data, language = 'en-IN', show_all = False)
            eel.process()
            print(data)
            return data
        except sr.RequestError as re:
            return ("API Call Fails", re)
        except sr.UnknownValueError as uve:
            return ("Can't Recognize", uve)
        except KeyboardInterrupt:
            return ("Keyboard Interrupt",)
        except Exception as e:
            return (e,)

def error_correction():
    data = speech_translation(False)
    if type(data) == tuple:
        return data
    # print('Error correction started!')
    oracle_std_dict = {
        'asterisk' : '*', 'character' : 'varchar2(25)', 'semicolon' : ';',
        'percentage': '%', (' comma', ' kama', ' Kama') : ',', 'greater than' : '>',
        'less than' : '<', ('equals', 'equal') : '=', 'greater than or equal to' : '>=',
        'less than or equal to' : '<=', 'not equal to' : '<>', 'open bracket ' : '(',
        ' close bracket' : ')', ('single quote', 'single quote', 'single coat' ) : "'",
        ('double coat', 'double quote', 'double quotes') : '"', ' underscore ' : '_', 
        'some (' : 'sum(', 'has' : 'as'
    }
    command = data
    for k, v in oracle_std_dict.items():
        if type(k) == tuple:
            for lv in k:
                command = command.replace(lv, v)
        else:
            command = command.replace(k, v)

    if command[len(command) - 1] != ';':
        command += ';'
    
    #Case conversion
    temp_command = list(command.split())
    uc = temp_command.count('uppercase')    
    lc = temp_command.count('lowercase')    
    try:
        while uc != 0:
            i = temp_command.index('uppercase')
            temp_command[i + 2] = temp_command[i + 2].upper()
            temp_command.pop(i)
            uc -= 1
        while lc != 0:
            i = temp_command.index('lowercase')
            temp_command[i + 2] = temp_command[i + 2].upper()
            temp_command.pop(i)
            lc -= 1
    except Exception:
        pass

    command = ft.reduce(lambda a, b: a + ' ' + b, temp_command)
    del temp_command
    #

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

    print(command)
    return command

def strip_inside_quotes(cmd):
    final_command = ''
    s = False
    for i, v in enumerate(cmd):
            if v == "'" or v == '"':
                final_command += v
                if s == False:
                    s = True
                else:
                    s = False
            elif s == True and v.isspace() == True:
                continue
            else:
                final_command += v
    return final_command


@eel.expose
def oracle_connection(val):
        # print('Started Succesfully!')
        if val == '':
            val = error_correction()
        if type(val) == tuple:
            eel.startAlert(val[0])
        else:
            val = val.strip()
            # print('Excecuting our command!')
            if val[:6] == 'select':
                val = 'set lines 250 pagesize 250;\n' + val
            if username == 'sys':
                connect_command = f'sqlplus -S {username}/{password} as sysdba'
            else:
                connect_command = f'sqlplus -S {username}/{password}'
            process = subprocess.Popen(connect_command, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=None)
            process.stdin.write(val.encode('utf-8')) #passing command
            stdOutput,stdError = process.communicate()
            print(stdOutput.decode('utf-8'))
            process.stdin.close()
            eel.response(val)


    
@eel.expose
def login(u, p):
    global username, password
    username = u
    password = p
    try:
        if username == 'sys':
            conn = cxo.connect(username, password, 'localhost', cxo.SYSDBA)
        else:
            conn = cxo.connect(f'{username}/{password}@localhost')
        conn.close()
        eel.verifiedLogin(f'Welcome {username.capitalize()}')
    except cxo.DatabaseError:
        eel.error()    

@eel.expose
def logout():
    global username, password
    username, password = '', ''
    eel.closeit()

eel.start('index.html')

