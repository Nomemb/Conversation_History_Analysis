from keybert import KeyBERT
from transformers import BertModel
from tqdm import tqdm
import pandas as pd
import pprint


df = pd.read_json("../dataset/preprocessing/only_text_03.주문결제.json")

model = BertModel.from_pretrained('skt/kobert-base-v1')
km_model = KeyBERT(model)

keywords = []

# for sentence in tqdm(get_text_from_json()):
#     keywords.append(km_model.extract_keywords(sentence['base_line'], keyphrase_ngram_range=(2, 4), use_maxsum=True, top_n=4))

for index, sentence in tqdm(df.iterrows()):
    all_sentence = " ".join([s[2:] for s in sentence['texts']])
    keywords.append(
        km_model.extract_keywords(all_sentence,
                                  keyphrase_ngram_range=(2,3),
                                  use_maxsum=True,
                                  top_n=10))

pprint.pprint(keywords)
