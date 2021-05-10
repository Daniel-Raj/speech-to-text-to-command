import speech_recognition as sr, subprocess
def speech_translation():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration = 0.5)
            print("Speak now")
            audio_data = r.listen(source, phrase_time_limit = 15)

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
    defaults = {
        'asterisk'  : '*',
        'character' : 'varchar2',
        'semicolon' : ';',
        'percentage': '%',
        'comma'     : ','}
    list_of_data = list(data.split())
    command = ''
    active = 0
    for ind, lists in enumerate(list_of_data[:]):
        if lists.lower() in defaults:
            command += defaults[lists] + ' '
        elif lists.lower() in ['single', 'double']:
            next_val = list_of_data[ind + 1]
            if next_val.lower() in ['quote', 'quotes', 'coat']:
                if lists.lower() == 'single':
                    if active == 0:
                        command += "'"
                        active = 1
                    else:
                        command = command.strip() + "'" + ' '
                        active = 0  
                else:
                    if active == 0:
                        command += '"'
                        active = 1
                    else:
                        command = command.strip() + '"' + ' '
                        active = 0
        elif lists.lower() in ['open', 'close']:
            next_val = list_of_data[ind + 1]
            if next_val == 'bracket':
                if lists == 'open':
                    command += '('
                else:
                    command += ')' + ' '
        elif lists in ['quote', 'quotes', 'coat', 'bracket']:
            continue
        else:
            command += lists + ' '
        command = command.replace('greater than', '>')
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
