import sys
import sh
import re
from eng_kaz_dic import eng_4_eng_kaz
from eng_kaz_dic import kaz_4_eng_kaz
from eng_kaz_dic import translate_with_dic

PATH_TO_APERTIUM = "/home/zhake/Source/apertium-eng-kaz"
TRANSLATION_DIRECTION = "eng-kaz"

# прочитать текст со входа
for line in sys.stdin:
    # ==========
    # сделать морфологический анализ и получить MorphLang_sl
    # ==========

    # print(sh.apertium(sh.echo(line), "-d", "/home/zhake/Source/apertium-eng-kaz", "eng-kaz-tagger"))
    morph_lang_sl = str(
        sh.apertium(
            sh.echo(line), "-d", PATH_TO_APERTIUM, TRANSLATION_DIRECTION + "-tagger"
        )
    )

    # ==========
    # разделить теги и слова
    # ==========

    # "очистка", чтобы слова разделялись только "$^"
    morph_lang_sl = re.sub(pattern="\$.+?\^", repl="$^", string=morph_lang_sl)

    # удаляем первый символ "^" и последний символ "$"
    morph_lang_sl = morph_lang_sl.strip()
    morph_lang_sl = morph_lang_sl[1:-1]

    # разбиваем строку на слова с тегами
    words_and_tags = morph_lang_sl.split("$^")

    # разделяем слова и теги
    for i in range(len(words_and_tags)):

        # добавляем пробел перед тегами для split
        words_and_tags[i] = re.sub(
            pattern="<", repl=" <", string=words_and_tags[i], count=1
        )

        # делаем split
        words_and_tags[i] = words_and_tags[i].split(maxsplit=1)

    # ==========
    # перевести слова по словарю
    # ==========

    # переводим те слова, которые не являются знаками препинания
    for i in range(len(words_and_tags)):
        if words_and_tags[i][1] != "<sent>":
            words_and_tags[i][0] = translate_with_dic(
                word=words_and_tags[i][0], direction=TRANSLATION_DIRECTION
            )

    print(words_and_tags)
    # ==========
    # сделать inference тегов с помощью обученной модели получить MorphLang_tl
    # ==========
    # ==========
    # объединить перевод слов и выведенных тегов
    # ==========
    # ==========
    # сделать морфологическую генерацию
    # ==========
    # ==========
    # вывести результат на stdout
    # ==========
