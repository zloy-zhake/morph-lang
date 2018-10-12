import sys
import sh
import re
import os
import os.path
from eng_kaz_dic import eng_4_eng_kaz
from eng_kaz_dic import kaz_4_eng_kaz
from eng_kaz_dic import translate_with_dic

# !! Необходим simlink на nmt в папке скрипта

PATH_TO_APERTIUM = "/home/zhake/Source/apertium-eng-kaz"
TRANSLATION_DIRECTION = "eng-kaz"
PATH_TO_MORPH_LANG_NMT_MODEL = "/media/zhake/Data/Универ/NMT/Experiments/МЯ с и без \
    сегментации/С сегментацией без слов/dataset/nmt_attention_model"

# прочитать текст со входа
for source_text_line in sys.stdin:
    # ==========
    # сделать морфологический анализ и получить MorphLang_sl
    # ==========

    # apertium -d '/home/zhake/Source/apertium-eng-kaz' eng-kaz-tagger
    morph_lang_sl = str(
        sh.apertium(
            sh.echo(source_text_line),
            "-d",
            PATH_TO_APERTIUM,
            TRANSLATION_DIRECTION + "-tagger",
        )
    )

    # весь текст в нижний регистр, так как словарь в нижнем регистре
    # до морфологического анализа делать не стоит, так как для него регистр важен
    morph_lang_sl = morph_lang_sl.lower()

    # ==========
    # разделить теги и слова
    # ==========

    # "очистка", чтобы слова разделялись только "$^"
    morph_lang_sl = re.sub(pattern="\$.+?\^", repl="$^", string=morph_lang_sl)

    # удаляем пробелы по краям, первый символ "^" и последний символ "$"
    morph_lang_sl = morph_lang_sl.strip()
    morph_lang_sl = morph_lang_sl[1:-1]

    # разбиваем строку на слова с тегами
    words_and_tags = morph_lang_sl.split("$^")

    # разделяем слова и теги
    for i in range(len(words_and_tags)):
        # делаем split
        # у слов со * нет анализов, поэтому им назначаем тег <unk>
        words_and_tags[i] = words_and_tags[i].split(sep="<", maxsplit=1)
        if len(words_and_tags[i]) == 1:
            words_and_tags[i].append("<unk>")

    # Восстанавливаем удаленную скобку
    for i in range(len(words_and_tags)):
        words_and_tags[i][1] = "<" + words_and_tags[i][1]

    # print(words_and_tags)
    # ==========
    # перевести слова по словарю
    # ==========

    # переводим те слова, которые не являются знаками препинания
    for i in range(len(words_and_tags)):
        if words_and_tags[i][1] != "<sent>":
            words_and_tags[i][0] = translate_with_dic(
                word=words_and_tags[i][0], direction=TRANSLATION_DIRECTION
            )

    # ==========
    # сегментировать теги
    # ==========
    for i in range(len(words_and_tags)):
        words_and_tags[i][1] = re.sub(
            pattern="><", repl="> <", string=words_and_tags[i][1]
        )

    # ==========
    # сделать inference тегов с помощью обученной модели получить MorphLang_tl
    # ==========

    # создать файл /tmp/input_infer
    # стираем старые данные, на случай, если они есть
    f = open(file="/tmp/input_infer", mode="w")
    f.close()

    # создать файл /tmp/output_infer
    # очищаем файл /tmp/output_infer
    f = open(file="/tmp/output_infer", mode="w")
    f.close()

    # добавляем новые данные
    for i in range(len(words_and_tags)):
        with open(file="/tmp/input_infer", mode="a") as input_inference_file:
            print(words_and_tags[i][1], file=input_inference_file)

    # сделать inference
    sh.bash("-c", "./inference.sh")

    # прочитать файл /tmp/output_infer
    with open(file="/tmp/output_infer", mode="r") as output_inference_file:
        for i in range(len(words_and_tags)):
            line = output_inference_file.readline()
            words_and_tags[i][1] = line

    # очистить ненужные символы "\n"
    for i in range(len(words_and_tags)):
        words_and_tags[i][1] = re.sub(
            pattern="\\n", repl="", string=words_and_tags[i][1]
        )

    # ==========
    # десегментировать теги
    # ==========
    for i in range(len(words_and_tags)):
        words_and_tags[i][1] = re.sub(pattern=" ", repl="", string=words_and_tags[i][1])

    # ==========
    # объединить перевод слов и выведенных тегов
    # ==========
    morph_lang_tl = ""
    for i in range(len(words_and_tags)):
        morph_lang_tl += "^"
        morph_lang_tl += words_and_tags[i][0]
        morph_lang_tl += words_and_tags[i][1]
        morph_lang_tl += "$ "

    # ==========
    # сделать морфологическую генерацию
    # ==========

    if TRANSLATION_DIRECTION == "eng-kaz":
        # hfst-proc $1 '/media/zhake/Data/apertium/Source/apertium-eng-kaz/eng-kaz.autogen.hfst'
        target_text_line = str(
            sh.hfst_proc(
                sh.echo(morph_lang_tl),
                "-g",
                PATH_TO_APERTIUM + "/" + TRANSLATION_DIRECTION + ".autogen.hfst",
            )
        )
    elif TRANSLATION_DIRECTION == "kaz-eng":
        # lt-proc $1 '/media/zhake/Data/apertium/Source/apertium-eng-kaz/kaz-eng.autogen.bin'
        target_text_line = str(
            sh.lt_proc(
                sh.echo(morph_lang_tl),
                "-g",
                PATH_TO_APERTIUM + "/" + TRANSLATION_DIRECTION + ".autogen.bin",
            )
        )

    # Очистить результат от диагностических символов Apertium
    target_text_line = re.sub(pattern="#|\*|@|~", repl="", string=target_text_line)

    # ==========
    # вывести результат на stdout
    # ==========

    print(target_text_line, end="")
