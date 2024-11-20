import pandas as pd
import json
from kiwipiepy import Kiwi

order_folder_path = "03.주문결제"
undo_folder_path = "05.환불반품교환"

df = pd.read_json("../dataset/preprocessing/05.환불반품교환.json")
#
result = []

# 객체 생성
kiwi = Kiwi()

for index, row in df.iterrows():
    lines = []
    base_tokenized_lines = []
    custom_tokenized_lines = []

    texts = []
    for line in row['info']['lines']:
        texts.append(line['text'])

    result.append({
        "index": index,
        "texts": texts
    })


def get_text_from_json():
    save_path = "../dataset/preprocessing/only_text_05.환불반품교환.json"
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


get_text_from_json()