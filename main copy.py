import eel, speech_recognition as sr, subprocess, cx_Oracle as cxo

eel.init('web')
username, password = '', ''

@eel.expose
def speech_translation(tostop):
    print('Listener is Ready!')
    if tostop != True:
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration = 0.5)
                eel.listen()
                audio_data = r.listen(source, phrase_time_limit = 15)

            data = r.recognize_google(audio_data, language = 'en-IN', show_all = False)
            print(data)
            return data
        except sr.RequestError as re:
            return ("API Call Fails :", re)
        except sr.UnknownValueError as uve:
            return ("Can't Recognize :", uve)
        except Exception as e:
            return (e,)

def error_correction():
    data = speech_translation(False)
    if type(data) == tuple:
        return data
    print('Error correction started!')
    oracle_std_dict = {
        'asterisk'  : '*', 'character' : 'varchar2(25)', 'semicolon' : ';',
        'percentage': '%', ' comma'     : ',', 'greater than' : '>',
        'less than' : '<', 'equals'    : '=', 'greater than or equal to' : '>=',
        'less than or equal to' : '<=', 'not equal' : '<>', 'open bracket' : '(',
        'close bracket' : ')', 'single quote' : "'", 'double quotes' : '"',
        'single quote' : "'", 'double quote' : '"', 'single coat' : "'",
        'double coat' : '"', ' underscore ' : '_'
    }
    command = data
    for k, v in oracle_std_dict.items():
        command = command.replace(k, v)
    if command[len(command) - 1] != ';':
        command += ';'
    print(command)
    return command

@eel.expose
def oracle_connection(val):
        print('Started Succesfully!')
        if val == '':
            val = error_correction()
        if type(val) == tuple:
            eel.startAlert(val[0], val[1])
        else:
            val = val.strip()
            print('Excecuting our command!')
            process = subprocess.Popen(f'sqlplus -S {username}/{password}', shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=None)
            process.stdin.write(val.encode('utf-8')) #passing command
            stdOutput,stdError = process.communicate()
            print(stdOutput.decode('utf-8'))
            process.stdin.close()
            eel.response(val)


@eel.expose
def kill():
    eel.verifiedLogin('')
    
@eel.expose
def login(u, p):
    global username, password
    username = u
    password = p
    try:
        conn = cxo.connect(f'{username}/{password}@localhost')
        conn.close()
        eel.verifiedLogin(f'Welcome {username}')
    except cxo.DatabaseError:
        eel.error()    

@eel.expose
def logout():
    global username, password
    username, password = '', ''
    eel.closeit()

eel.start('index.html')


