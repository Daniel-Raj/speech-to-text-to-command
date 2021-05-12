import speech_recognition as sr, subprocess
def speech_translation():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration = 0.5)
            print("Speak now")
            audio_data = r.listen(source, phrase_time_limit = 30)

        data = r.recognize_google(audio_data, language = 'en-IN', show_all = False)
        print(data)
        return data
    except sr.RequestError as re:
        print("API Call Fails :", re)
    except sr.UnknownValueError as uve:
        print("Can't Recognize :", uve)
    except Exception as e:
        print(e)

def error_correction():
    data = speech_translation()

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

def oracle_connection():
    val = error_correction().strip()
    process = subprocess.Popen('sqlplus -S scott/tiger', shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=None)
    process.stdin.write(val.encode('utf-8')) #passing command
    stdOutput,stdError = process.communicate()
    print(stdOutput.decode('utf-8'))
    process.stdin.close()

if __name__ == '__main__':
    print('''Use the following PHRASES for the values while speaking
            _________________________       
            Phrases       - values
            -------------------------
            Open bracket  - (
            Close bracket - )
            Asterisk      - *
            Character     - varchar2
            equals        - =''')
    error_correction()
    # oracle_connection()
