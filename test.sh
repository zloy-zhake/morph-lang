
# активируем виртуальное окружение для tensorflow
source /media/zhake/Data/venvs/tf-gpu/bin/activate

python -c "import tensorflow as tf; print(tf.__version__)"

# деактивируем виртуальное окружение
deactivate
