import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# JSON 파일을 로드하는 함수 정의
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# 데이터 준비 함수
def prepare_data(json_data):
    # "원문"을 텍스트로 사용하고 "카테고리"를 레이블로 사용
    texts = [entry['원문'] for entry in json_data]
    labels = [entry['카테고리'] for entry in json_data]
    return pd.DataFrame({'text': texts, 'label': labels})

# 모델 학습 함수
def train_model(train_data):
    # 벡터화 (CountVectorizer로 텍스트를 수치로 변환)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(train_data['text'])
    y = train_data['label']
    
    # 모델 학습
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
    train_json = load_json(train_json_file)
    test_json = load_json(test_json_file)
    
    # 데이터 준비
    train_data = prepare_data(train_json)
    test_data = prepare_data(test_json)
    
    # 모델 학습
    model, vectorizer = train_model(train_data)
    
    # 모델 평가
    evaluate_model(model, vectorizer, test_data)

# 파일 경로 지정
train_file = 'train_data.json'
test_file = 'test_data.json'

# 실행
main(train_file, test_file)
