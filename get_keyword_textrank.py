import json
import pandas as pd
from krwordrank.word import summarize_with_keywords
from tokenizing import dialog_dict


# with open("./tokenized_morphs.json", "r", encoding='utf-8') as f:
#     data = json.load(f)

data = dialog_dict
df_list = []
penalty = lambda x: 0 if (25 <= len(x) <= 80) else 1
stopwords = {'고객', '아니', '고객님', '지금', '그럼', '아니면', '안녕하세요', '제가', '되어', '혹시', '상담원', '입니', '안녕', '감사합니다', '감사', '경우',
             '통해', '으로', '알겠습니다', '한번', '알겠습니다', '확인', '추후에', '하겠습니다', '어떤', '바로', '네네', '이나', '많이', '되세요', '수고하세요',
             '말씀'}

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

label_dict = {
    '가입문의' : 0,
    '요금문의' : 1,
    '서비스변경' : 2,
    '고장신고' : 3,
    '해지' : 4
}