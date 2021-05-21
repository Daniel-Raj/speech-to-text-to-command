import eel, speech_recognition as sr, subprocess
import cx_Oracle as cxo, time
import err_corr as ec

eel.init('web')
username, password = '', ''

@eel.expose
def speech_translation():
    # print('Listener is Ready!')    
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration = 0.2)
            eel.ack()
            audio_data = r.listen(source, phrase_time_limit=20)

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

@eel.expose
def oracle_connection(val):
        # print('Started Succesfully!')
        if val == '':
            val = ec.error_correction(speech_translation())
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
    eel.ack('Verifying')
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
        time.sleep(1)
        eel.error()
        eel.closeit()
        
        
         

@eel.expose
def logout():
    global username, password
    username, password = '', ''
    eel.closeit()

eel.start('index.html')

