import json
import os
import nltk
from nltk.tokenize import word_tokenize

# nltk 리소스 다운로드 (최초 한 번만 실행)
nltk.download('punkt')
nltk.download('punkt_tab')

# 경로 설정
file_path = "C:/Users/Admin/Desktop/프로젝트_11월2차/Conversation_History_Analysis/data/금융_상품 가입 및 해지.json"

# JSON 파일 읽기
with open(file_path, "r", encoding='utf-8') as json_file:
    data = json.load(json_file)

'''
# JSON 데이터를 보기 좋게 출력
    formatted_data = json.dumps(data,  indent=4, ensure_ascii=False)
 
 # "고객답변"과 "상담사답변" 키 값 토큰화
    customer_responses = []
    consultant_responses = []

    for entry in data:
        # "고객답변"과 "상담사답변"이 존재하는 경우
        customer_answer = entry.get("고객답변")
        consultant_answer = entry.get("상담사답변")
        # "고객질문(요청)"과 "상담사질문(요청)"이 존재하는 경우
        customer_question = entry.get("고객질문(요청)")
        consultant_question = entry.get("상담사질문(요청)")

        if customer_answer:
            customer_tokens = word_tokenize(customer_answer)
            entry["고객답변"] = customer_tokens

        if consultant_answer:
            consultant_tokens = word_tokenize(consultant_answer)
            entry["상담사답변"] = consultant_tokens

        if customer_question:
            customer_tokens = word_tokenize(customer_question)
            entry["고객질문(요청)"] = customer_tokens

        if consultant_question:
            consultant_tokens = word_tokenize(consultant_question)
            entry["상담사질문(요청)"] = consultant_tokens

    # JSON 데이터 보기 좋게 출력
    formatted_data = json.dumps(data, indent=4, ensure_ascii=False)
    print(formatted_data)
'''

# 대화셋 일련번호 기준으로 묶기
grouped_data = {}

for entry in data:
    conversation_id = entry.get("대화셋일련번호")
    if conversation_id:
        # 대화셋일련번호 기준으로 문장을 묶음
        if conversation_id not in grouped_data:
            grouped_data[conversation_id] = []
        grouped_data[conversation_id].append(entry)

# 문장번호 기준으로 정렬
for conversation_id in grouped_data:
    grouped_data[conversation_id] = sorted(grouped_data[conversation_id], key=lambda x: x.get("문장번호", 0))

# 일부 결과 확인
formatted_data = json.dumps(grouped_data, indent=4, ensure_ascii=False)
print(formatted_data)
