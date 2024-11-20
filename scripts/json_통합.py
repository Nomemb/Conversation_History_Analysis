import pandas as pd
import os
import json


def get_text_info(info):
    info_list = []
    for i in info:
        data = {
            "id": i["id"],
            "text": i["text"],
            "speechAct": i["speechAct"],
            "morpheme": i["morpheme"]
        }
        info_list.append(data)
    return info_list


def convert(add_path):
    base_folder_path = "C:/Users/Admin/Desktop/Conversation_History_Analysis/dataset/"
    preprocessing_list = []
    folder_path = base_folder_path + add_path
    for file in os.listdir(folder_path):
        file_path = f"{folder_path}/{file}"
        with open(file_path, encoding='utf-8') as f:
            d = json.load(f)
            preprocessing_list.append({
                "dataset_path":file_path,
                "info": {
                    "category": d["info"][0]["category"],
                    "lines": get_text_info(d["info"][0]["annotations"]["lines"])
                }
            })

    save_path = f"{base_folder_path}/preprocessing/{add_path}.json"
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(preprocessing_list, f, indent=4, ensure_ascii=False)


order_folder_path = "03.주문결제"
undo_folder_path = "05.환불반품교환"

convert(order_folder_path)
convert(undo_folder_path)