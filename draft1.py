import speech_recognition as sr
def speech_translation():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration = 0.5)
            print("Speak now")
            audio_data = r.listen(source)

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
        'asterisk' : '*',
        'character': 'varchar2'}
    list_of_data = list(data.split())
    for ind, lists in enumerate(list_of_data[:]):
        if lists in defaults:
            list_of_data[ind] = defaults[lists]
    command = ''
    for val in list_of_data:
        command += val + ' '
    print(command.strip())

def oracle_connection():
    pass

if __name__ == '__main__':
    print('''Use the following alternate phrases while speaking....
            _________________________       
            Phrases       - values
            -------------------------
            Open Bracket  - (
            Close Bracket - )
            Asterisk      - *
            Comma         - ,
            Character     - varchar2''')
    error_correction()
