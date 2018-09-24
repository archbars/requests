import requests
import os


def translate_it(text, input_lang, output_lang):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    # key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
    key = 'trnsl.1.1.20180924T094943Z.6cb642fa2d55a5ed.0a4883a4ad71ac1f12ec3e0c1d7a495a8416e071'

    params = {
        'key': key,
        'lang': input_lang+"-"+output_lang,
        'text': text,
    }

    response = requests.get(url, params=params).json()
    return ' '.join(response.get('text', []))


def language_detect(text):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
    # key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
    key = 'trnsl.1.1.20180924T094943Z.6cb642fa2d55a5ed.0a4883a4ad71ac1f12ec3e0c1d7a495a8416e071'

    params = {
        'key': key,
        'text': text,
    }
    response = requests.get(url, params=params).json()
    return response.get('lang')


def for_files_in_folder():
    for d, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), "input")):
        for file in files:
            source_file = os.path.join(d, file)
            destination_file = os.path.join(os.path.join(os.path.dirname(__file__), "output"), file)
            with open(source_file, 'r') as curfile:
                for line in curfile:
                    if len(line) > 1:
                        cur_lang = language_detect(line)
                        with open(destination_file, 'a') as destfile:
                            destfile.write(translate_it(line, cur_lang, "ru"))
                    else:
                        with open(destination_file, 'a') as destfile:
                            destfile.write('\n')


for_files_in_folder()


