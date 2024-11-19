import json
import joblib
from sklearn.metrics import accuracy_score, classification_report

# 테스트 데이터 경로 및 로드
test_data_path = 'C:/Users/Admin/Desktop/프로젝트_11월2차/Conversation_History_Analysis/data/test_data.json'
with open(test_data_path, 'r', encoding='utf-8') as file:
    test_data = json.load(file)

# 테스트 데이터에서 텍스트와 레이블 추출
X_test = [item["패딩된 형태소 분석 결과"] for item in test_data]  # 형태소 분석 결과
y_test = [item["대화셋일련번호"] for item in test_data]  # 대화셋 일련번호 (또는 적절한 레이블)

# 저장된 모델 로드
model = joblib.load('text_classifier_model.pkl')

# 예측 수행
y_pred = model.predict(X_test)

# 모델 평가 (정확도 및 리포트)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

