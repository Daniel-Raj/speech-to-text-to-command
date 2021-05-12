import eel

eel.init('web')

@eel.expose
def start():
    eel.transform()

eel.start('index.html')

