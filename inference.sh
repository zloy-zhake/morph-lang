
# активируем виртуальное окружение для tensorflow
source /media/zhake/Data/venvs/tf-gpu/bin/activate

# делаем inference
python -m nmt.nmt \
--out_dir="./С сегментацией без слов/dataset/nmt_attention_model" \
--inference_input_file=/tmp/input_infer \
--inference_output_file=/tmp/output_infer

# деактивируем виртуальное окружение
deactivate
