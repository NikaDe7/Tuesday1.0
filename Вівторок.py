import os
import sys
import random
import wikipedia
import speech_recognition
import pyttsx3
import datetime
import webbrowser
import pyowm
import sqlite3
from pyowm.utils.config import get_default_config 
import cowsay
import pyautogui
import pyjokes
import randfacts
from googletrans import Translator

# 'sapi5'
translator = Translator()
sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5
sr.energy_threshold = 4000
sr.dynamic_energy_adjustment_ratio = 5
engine = pyttsx3.init()
engine.setProperty('voice', 'uk-UA')
hour = int(datetime.datetime.now().hour)
config_dict = get_default_config()
config_dict['language'] = 'uk'
owm = pyowm.OWM('21c66c39fdafae690ceae27bdfcc47f0', config_dict)
mgr = owm.weather_manager()
connect = sqlite3.connect('db/baza.db')
cursor = connect.cursor()

commands_dict = {
    'commands': {
        'greeting': ['привіт вівторок', 'добрий день вівторок', 'привіт'],
        'create_tack': ['додати задачу', 'додати замітку'],
        'play_music': ['музика', 'включи музику', 'музику'],
        'wiki': ['включи вікіпедію', 'вікіпедія'],
        'youTB': ['включи відео', 'пошук відео', 'відео'],
        'browser': ['відкрий браузер', 'хром','браузер','пошук'],
        'time': ['яка година', 'котра година'],
        'weather': ['погода', 'яка зараз погода'],
        'bye':['іти спати', 'бувай', 'добраніч','до зустрічі'],
        'tomorrow':['яка завтра погода', 'пророцтво','що буде завтра'],
        'thank':['дякую','превелике дякую'],
        'call':['калькулятор','відкрий калькулятор'],
        'ball':['час гри','гра'],
        'screen':['зроби фото',' зроби скрін','екран'],
        'joke':['анекдот','розкажи анекдот'],
        'story':['розкажи історію','історія'],
        'facts':['розкази факт','факт']
    }
}

def listen_command():
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='uk-UA').lower()
            return query
    except speech_recognition.UnknownValueError:
        speak('Нічого не зрозумів')
        cowsay.cow('Нічого не зрозумів')

class VoiceAssistant:
    voices = engine.getProperty('voices')
    # швидкість
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 200)
    # гучність
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 1)
    # мова за замовчуванням
    engine.setProperty('voice', 'uk-UA')
    # голос
    for voice in voices:
        if voice.name == 'Anatol':
           engine.setProperty('voice', voice.id)

def speak(listen_command):
    engine.say(listen_command)
    engine.runAndWait()
       
def greeting():
    if hour >= 0 and hour < 12:
        speak('Як не дивно, але Доброго ранку')
        return f'Як не дивно, але Доброго ранку'
    elif hour>=12 and hour<18:
        speak('День добрий')
        return f'День добрий'
    else:
        speak('Вечір в хату')
        return f'Вечір в хату'

def thank():
    speak('прошу, чим займемся дальше?')
    return f'Прошу, чим займемся дальше?'

def joke():
    joke = pyjokes.get_joke()
    a = translator.translate(joke, dest='uk')
    speak(a.text)
    return f'{a.text}'
#∙
def create_tack():
    speak('Що дописати до заміток?')
    print('Що дописати до заміток?')
    query = listen_command()
    with open('list.txt', 'a') as file:
        file.write(f'* {query}\n')
    speak('Замітка')
    speak(query)
    speak('додана до списку')
    return f'Замітка {query} додана до списку!'

def play_music():
    files = os.listdir('music')
    random_file = f'music/{random.choice(files)}'
    speak('Слухаєм')
    speak(random_file.split("/")[-1])
    os.system(f'start {random_file}')
    return f'Слухаєм {random_file.split("/")[-1]}'

def wiki():
    speak('Що шукати у Вікіпедії?')
    print('Що шукати у Вікіпедії?')
    query = listen_command()
    wikipedia.set_lang("uk") 
    wikip = wikipedia.page(query).content
    speak('Згідно з вікіпедією ')
    speak(wikip)
    return f'{wikip}'

def youTB():
    print('Що шукати?')
    speak('Що шукати?')
    search_term = listen_command()
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open(url)
    speak('Зайдіть до вашого браузера')
    return f'Зайдіть до вашого браузера'

def browser():
    print('Що шукати?')
    speak('Що шукати?')
    r=listen_command()
    url = "https://www.google.com/search?q=" + r
    webbrowser.get().open(url)
    speak('Зайдіть до вашого браузера')
    return f'Зайдіть до вашого браузера'

def weather():
    observation= mgr.weather_at_place('Lviv, UA')
    w = observation.weather
    print('Статус на сьогодні')
    speak('Подивіться на результат')
    data = {
        '[Загалом]':w.detailed_status,
        '[Швидкість повітря{м/с)]':w.wind()['speed'],
        '[Температура(С°)]':w.temperature('celsius')['temp'],
        '[Вологість(%)]':w.humidity,
        '[Хмарність(%)]':w.clouds}
    for u,h in data.items():
        print(f'{u} : {h}')
    print ('Це все')
    speak('Це все')
    print('Вам цікаво, що буде завтра?')
    speak('Вам цікаво, що буде завтра?')
    j=['звичайно','так','давай']
    n=listen_command()
    if n in j:
        tomorrow()
        return f'Ще щось?'
    else:
        speak('Як скажете')
        return f'Як скажете' 

def tomorrow():
    speak('Я бачу майбутьнє')
    print('Cтатус на завтра')
    one_call = mgr.one_call(lat=47.8932, lon=31.0913)
    speak('Подивіться на результат')
    dat = {
        '[Статус]':one_call.forecast_daily[0].detailed_status,
        '[Швидкість повітря(м/с)]':one_call.forecast_daily[0].wind()["speed"],
        '[Температура(С°)]':one_call.forecast_daily[0].temperature('celsius').get('day', None),
        '[Вологість(%)]':one_call.forecast_daily[0].humidity,
        '[Хмарність(%)]':one_call.forecast_daily[0].clouds
    }
    for m,n in dat.items():
        print(f'{m} : {n}')
    speak('Тепер ти знаєщ, шо буде завтра')
    return f'Це все'


def time():
    strTime = datetime.datetime.now().strftime('%H:%M')
    speak('Зараз')
    speak(strTime)
    return f'Зараз {strTime}'

def facts():
    f = randfacts.get_fact(False)
    a= translator.translate(f, dest='uk')
    speak(a.text)
    return f'{a.text}'

def call():
    speak('Час математики')
    q1 =float(input('Введіть число 1: '))
    q2 =float(input('Введіть число 2: '))
    print('Список дій: 1. Додавання, 2. Віднімання, 3. Ділення, 4. Множення')
    v =int(input('Виберіть дію:'))
    if v == 1:
        r = q1 + q2
        p = 'додавання'
        t = p
    if v == 2:
        r = q1 - q2
        l = 'віднімання'
        t = l
    if v == 3:
        r = float(q1 / q2)
        m = 'ділення'
        t = m
    if v == 4:
        r = q1 * q2
        n = 'множення'
        t = n
    speak('Відповідь:')
    speak(r)
    return f'Результат {t} = {r}'

def bye():
    speak('До зустрічі')
    print('До зустрічі')
    sys.exit()

def ball():
    speak('Кристальний шар баче майбутьнє')
    speak('Задавайте питання')
    while True:
        a=['кінець', 'дякую за магію','стоп']
        b=listen_command()
        h='Ти найкращий?'
        if b in a:
            break
        elif b == ' ':
            continue
        elif h==b:
            print('Так')
            speak('так')
        else:
            k=['Так','Ні','Можливо','Не знаю']
            x=random.choice(k)
            speak(x)
            print(x)
    speak('Сеанс закінчено')
    return 'Сеанс закінчено'

def screen():
    strTime = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')
    im1 = pyautogui.screenshot()
    x=str(strTime)+'.png'
    im1.save(r'C:\Users\vorob\OneDrive\Рабочий стол\Вівторок\screen_shout\screen_'+x)
    speak('Готово')
    return 'Готово'

def story():
    Sentence_starter = ['Сто років вперед,', 'Діло буде в 41 році,', 'В один прекрасний період часу,']
    character = [' житиме король.',' житиме фермер.', ' житиме Антон.', ' житиме Маргарет.']
    time = [' В один прекрасний день', ' Опівночі', ' Після обіду']
    story_plot = [', роздумуючи про життя,',', йшовши на пікнік,']
    place = [' в горах,', ' в саду,', ' на озері,']
    second_character = [' бачить чоловіка.', ' побачить незнайомку.']
    work = [' Коли стало нудно,', ' Коли стало цікаво,']
    run = [' захотілось спитатися, "як звати"?, але людина вже втекла.']
    end = [' Не вийде зустрітись їм знову навіть, коли',' Зустрінуться вони, коли']
    tim = [' пройде 100 років',' настане час']

    m=random.choice(Sentence_starter)+random.choice(character)+random.choice(time)+random.choice(story_plot)+random.choice(place)+random.choice(second_character)+random.choice(work)+random.choice(run)+random.choice(end)+random.choice(tim)
    print(m)
    speak(m)
    speak('Кінець')
    return 'Кінець'

def db_plus():
    cursor.execute(""" CREATE TABLE IF NOT EXISTS expenses(name TEXT, password INTEGER) """)
    connect.commit()

def db_list():
    a=input("Введіть ім'я:")
    b=input("Введіть пароль:")
    main_list=[a, b]
    cursor.execute("INSERT INTO expenses VALUES(?,?);",main_list)
    connect.commit()

def avto():
    print('Авторизуйтесь, будь ласка')
    name=input("Введіть ім'я:")
    pas=int(input("Введіть пароль:"))
    result=cursor.execute("SELECT * FROM expenses").fetchall()
    for row in result:
        names=row[0]
        pasw=row[1]
    if name==names and pas==pasw:
        greeting()
        print('Чим сьогодні займемся?')
        speak('Чим сьогодні займемся?')
        main()
    else:
        cowsay.cow('Ви хто?')
        speak('Ви хто?')
        cowsay.cow ('Хоча, бувайте')
        speak('Хоча, бувайте')
    
def main():
    while True:
        query=listen_command()
        for k, v in commands_dict['commands'].items():
            if query in v:
                print(globals()[k]())
        if query == ' ':
            continue

if __name__=='__main__':
    x = datetime.datetime.now().strftime("%a")
    if x=="Mon":
        print("Ви зареєстровані? т/н")
        c=input("Введіть відповідь:")
        if c == 'т':
            avto()
        if c == 'н':
            db_plus()
            db_list()
            avto()
    else:
        greeting()
        print('Чим сьогодні займемся?')
        speak('Чим сьогодні займемся?')
        main()
