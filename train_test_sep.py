import json
import random
from sklearn.model_selection import train_test_split

# JSON 파일 경로 및 읽기
input_path = 'C:/Users/Admin/Desktop/프로젝트_11월2차/Conversation_History_Analysis/data/output_with_padding_and_category.json'
with open(input_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 데이터를 "대화셋일련번호" 기준으로 리스트로 변환
conversation_list = []
for conversation_id, items in data.items():
    for item in items:
        conversation_list.append({
            "대화셋일련번호": conversation_id,
            "원문": item["원문"],
            "형태소 분석 결과": item["형태소 분석 결과"],
            "패딩된 형태소 분석 결과": item["패딩된 형태소 분석 결과"],
            "카테고리": item.get("카테고리", "기타")  # 카테고리 정보 추가, 없으면 '기타'로 처리
        })

# train/test 분할 (80%는 train, 20%는 test)
train_data, test_data = train_test_split(conversation_list, test_size=0.2, random_state=42)

# train과 test 데이터를 각각 JSON 파일로 저장
train_output_path = 'C:/Users/Admin/Desktop/프로젝트_11월2차/Conversation_History_Analysis/data/train_data.json'
test_output_path = 'C:/Users/Admin/Desktop/프로젝트_11월2차/Conversation_History_Analysis/data/test_data.json'

# Train 데이터 저장
with open(train_output_path, 'w', encoding='utf-8') as train_file:
    json.dump(train_data, train_file, ensure_ascii=False, indent=4)

# Test 데이터 저장
with open(test_output_path, 'w', encoding='utf-8') as test_file:
    json.dump(test_data, test_file, ensure_ascii=False, indent=4)

print("Train 데이터와 Test 데이터가 저장되었습니다.")
