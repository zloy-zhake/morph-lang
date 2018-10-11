import sys
import sh
import re

# прочитать текст со входа
for line in sys.stdin:
    # ==========
    # сделать морфологический анализ и получить MorphLang_sl
    # ==========

    # print(sh.apertium(sh.echo(line), "-d", "/home/zhake/Source/apertium-eng-kaz", "eng-kaz-tagger"))
    morph_lang_sl = str(
        sh.apertium(
            sh.echo(line), "-d", "/home/zhake/Source/apertium-eng-kaz", "eng-kaz-tagger"
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
        words_and_tags[i] = re.sub(pattern="<", repl=" <", string=words_and_tags[i], count=1)
        # делаем split
        words_and_tags[i] = tuple(words_and_tags[i].split(maxsplit=1))
    print(words_and_tags)

    # ==========
    # перевести слова по словарю
    # ==========
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
