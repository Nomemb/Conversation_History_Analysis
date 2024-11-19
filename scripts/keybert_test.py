from keybert import KeyBERT
from transformers import BertModel
from tqdm import tqdm
import pandas as pd


def extract_keywords(file_path, model):
    keywords = []
    df = pd.read_json(file_path)

    km_model = KeyBERT(model)

    cnt = 0
    for index, sentence in tqdm(df.iterrows()):
        cnt += 1
        if cnt > 100:
            break
        all_sentence = " ".join([s[2:] for s in sentence['texts']])
        keywords.append(
            km_model.extract_keywords(all_sentence,
                                      keyphrase_ngram_range=(1,2),
                                      use_maxsum=True,
                                      top_n=4))

    return keywords, df
