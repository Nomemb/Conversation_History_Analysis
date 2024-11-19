import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# JSON 파일 경로 및 읽기
train_data_path = 'C:/Users/Admin/Desktop/프로젝트_11월2차/Conversation_History_Analysis/data/train_data.json'
test_data_path = 'C:/Users/Admin/Desktop/프로젝트_11월2차/Conversation_History_Analysis/data/test_data.json'

with open(train_data_path, 'r', encoding='utf-8') as file:
    train_data = json.load(file)
    
with open(test_data_path, 'r', encoding='utf-8') as file:
    test_data = json.load(file)

# 데이터 준비 함수
def prepare_data(json_data):
    texts = []
    labels = []
    
    for entry in json_data:
        # 형태소 분석 결과를 하나의 문자열로 결합하여 텍스트로 사용
        text = " ".join(entry['형태소 분석 결과'])
        category = entry['카테고리']  # "카테고리"를 레이블로 사용
        texts.append(text)
        labels.append(category)
    
    return pd.DataFrame({'text': texts, 'label': labels})

# 모델 학습 함수
def train_model(train_data):
    # 벡터화 (CountVectorizer로 텍스트를 수치로 변환)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(train_data['text'])
    y = train_data['label']
    
    # 모델 학습 (로지스틱 회귀 모델 사용)
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X, y)
    
    return model, vectorizer

# 모델 평가 함수
def evaluate_model(model, vectorizer, test_data):
    X_test = vectorizer.transform(test_data['text'])
    y_test = test_data['label']
    y_pred = model.predict(X_test)
    
    # 성능 평가
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

# 메인 함수
def main(train_json_file, test_json_file):
    # 데이터 로드
    train_data = prepare_data(train_json_file)
    test_data = prepare_data(test_json_file)
    
    # 모델 학습
    model, vectorizer = train_model(train_data)
    
    # 모델 평가
    evaluate_model(model, vectorizer, test_data)

# 실행
main(train_data, test_data)
