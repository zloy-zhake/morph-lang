import sys
import sh

# прочитать текст со входа
for line in sys.stdin:

    # сделать морфологический анализ и получить MorphLang_sl
    print(sh.apertium(sh.echo(line), "-d", "/home/zhake/Source/apertium-eng-kaz", "eng-kaz"))

# сделать inference с помощью обученной модели получить MorphLang_tl
# сделать морфологическую генерацию