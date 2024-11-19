import json
import pandas as pd
import re
import numpy as np
from krwordrank.word import summarize_with_keywords
from tokenizing import dialog_dict


# with open("./tokenized_morphs.json", "r", encoding='utf-8') as f:
#     data = json.load(f)

data = dialog_dict

stopwords = {'고객', '아니', '고객님', '지금', '그럼', '아니면', '안녕하세요', '제가', '되어', '혹시', '상담원', '입니', '안녕', '감사합니다', '감사', '경우',
             '통해', '으로', '알겠습니다', '한번', '알겠습니다', '확인', '추후에', '하겠습니다', '어떤', '바로', '네네', '이나', '많이', '되세요', '수고하세요',
             '말씀'}

### 통합 dictionary로부터 keyword 추출 및 DataFrame화
df_list = []
for key in list(data.keys()):
    text_list = []
    keyword_list = []
    for idx in range(len(data[key])):
        text_list.append(data[key][idx]['text'].strip())
        try:
            keywords = list(
                summarize_with_keywords(data[key][idx]['lines'], verbose=False, num_keywords=50, stopwords=stopwords,
                                        min_count=2, beta=0.85, max_iter=10).keys())[:3]
            keyword_list.append(keywords)
        except:
            keywords = 0
            print(idx)
            keyword_list.append(keywords)

    df = pd.DataFrame({
        'category': [key] * len(text_list),  # 'category' 열 생성
        'text': text_list,  # 'text' 열 생성
        'keyword': keyword_list
    })
    df_list.append(df)

df_total = pd.concat(df_list, axis=0).reset_index(drop=True)

### text 기반 labelling 진행 - Label Encoding
label_dict = {
    '가입문의' : 0,
    '요금문의' : 1,
    '서비스변경' : 2,
    '고장신고' : 3,
    '해지' : 4
}

def get_label(txt):
    label_one_len = len(re.findall(r'[가-힣]*결제[가-힣]*', txt)) + len(re.findall(r'[가-힣]*주문[가-힣]*', txt))
    label_two_len = len(re.findall(r'[가-힣]*환불[가-힣]*', txt)) + len(re.findall(r'[가-힣]*취소[가-힣]*', txt)) + len(re.findall(r'[가-힣]*삭제[가-힣]*', txt)) + len(re.findall(r'[가-힣]*반품[가-힣]*', txt))
    label_three_len = len(re.findall(r'[가-힣]*교체[가-힣]*', txt)) + len(re.findall(r'[가-힣]*교환[가-힣]*', txt))
    label_four_len = len(re.findall(r'[가-힣]*얼마[가-힣]*', txt)) + len(re.findall(r'[가-힣]*교환[가-힣]*', txt))
    label_five_len = len(re.findall(r'[가-힣]*사용[가-힣]*', txt)) + len(re.findall(r'[가-힣]*이용[가-힣]*', txt))
    label_len_arr = np.array([label_one_len, label_two_len, label_three_len, label_four_len, label_five_len])
    max_label = label_len_arr.max()
    if max_label == label_one_len:
        return '가입문의'
    elif max_label == label_two_len:
        return '해지'
    elif max_label == label_three_len:
        return '서비스변경'
    elif max_label == label_four_len:
        return '요금문의'
    elif max_label == label_five_len:
        return '서비스문의'
    else:
        return None

for idx, row in df_total.iterrows():
    txt = row['text']
    row['label'] = get_label(txt)

df_total.dropna(inplace=True)
df_total['num_label'] = df_total.label.map(label_dict)

### 부가적인 옵션 (라벨 인코딩 시 sklearn Label Encoder 사용)
# from sklearn.preprocessing import LabelEncoder
# le = LabelEncoder()
# le.fit(df_total.label)
# le_encoded = le.transform(df_total.label)
# df_total = pd.DataFrame(le_encoded, columns = ['result'])
# df_total['label_num'] = le_encoded