import speech_recognition as sr
import webbrowser

r =sr.Recognizer()

with sr.Microphone() as source:
    print('Speak Something: ')
    audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print('You said: {}'.format(text))
        url = "https://google.com/search?q="+text
        webbrowser.get().open(url)
    except:
        print('Error occured')

