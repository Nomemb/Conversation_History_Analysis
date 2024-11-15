import pandas as pd
import pprint
import json
from kiwipiepy import Kiwi
from konlpy.tag import Okt, Komoran, Hannanum

order_folder_path = "03.주문결제"
undo_folder_path = "05.환불반품교환"

df = pd.read_json("../dataset/preprocessing/03.주문결제.json")
#
result = []

# 객체 생성
kiwi = Kiwi()

cnt, max_cnt = 0, 10
for index, row in df.iterrows():
    cnt += 1
    if cnt > max_cnt:
        break
    lines = []
    base_tokenized_lines = []
    custom_tokenized_lines = []

    texts = []
    for line in row['info']['lines']:
        texts.append(line['text'])
        # morph_list = kiwi.tokenize(line['text'])
        #
        # result.append({
        #     "base_line": line['text'],
        #     "base_tokenized_line": line['morpheme'],
        #     "custom_tokenized_line": '+'.join([f"{morph[0]}/{morph[1]}" for morph in morph_list])
        # })
    result.append({
        "index": index,
        "texts": texts
    })

def get_text_from_json():
    save_path = "../dataset/preprocessing/only_text_03.주문결제.json"
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


get_text_from_json()