import json
import os
import nltk
from nltk.tokenize import word_tokenize
from kiwipiepy import Kiwi, Match

# Kiwi 초기화
kiwi = Kiwi()
Kiwi(num_workers=2,
    load_default_dict=True,
    integrate_allomorph=True)

# JSON 파일 읽기
file_path = 'C:/Users/Admin/Desktop/프로젝트_11월2차/Conversation_History_Analysis/data/금융_상품 가입 및 해지.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# JSON 데이터에서 텍스트 추출 및 형태소 분석
if isinstance(data, dict):  # JSON이 딕셔너리 형식인 경우
    texts = data.get('texts', [])  # 'texts' 키에 텍스트 데이터가 있다고 가정
elif isinstance(data, list):  # JSON이 리스트 형식인 경우
    texts = data

# 형태소 분석
for text in texts:
    result = kiwi.analyze(text)
    print(f"원문: {text}")
    for sentence in result:
        print(f"분석 결과: {sentence}")


'''
# nltk 리소스 다운로드 (최초 한 번만 실행)
nltk.download('punkt')
nltk.download('punkt_tab')

# 경로 설정
file_path = "C:/Users/Admin/Desktop/프로젝트_11월2차/Conversation_History_Analysis/data/금융_상품 가입 및 해지.json"

# JSON 파일 읽기
with open(file_path, "r", encoding='utf-8') as json_file:
    data = json.load(json_file)


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
