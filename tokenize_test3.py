import json
import os
from kiwipiepy import Kiwi
from collections import defaultdict

# kiwi 초기화
kiwi = Kiwi(num_workers=2, load_default_dict=True, integrate_allomorph=True)

# JSON 파일 경로 및 읽기
file_path = 'C:/Users/Admin/Desktop/프로젝트_11월2차/Conversation_History_Analysis/data/금융_상품 가입 및 해지.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 분석 대상 키
target_keys = {"고객질문(요청)", "상담사질문(요청)", "고객답변", "상담사답변"}

# 형태소 분석 결과 저장
analysis_results = defaultdict(list)

# "대화셋일련번호" 기준으로 데이터 그룹화
grouped_data = defaultdict(list)

# 텍스트 패딩을 위한 함수
def pad_text_to_max_length(texts):
    # 텍스트 중 가장 긴 길이 계산
    max_length = max(len(text.split()) for text in texts)
    
    padded_texts = []
    for text in texts:
        words = text.split()  # 공백으로 단어 분리
        if len(words) < max_length:
            # 부족한 길이는 공백으로 패딩
            padded_text = words + [''] * (max_length - len(words))
        else:
            # 길이가 충분하면 자르기
            padded_text = words[:max_length]
        padded_texts.append(" ".join(padded_text))
    
    return padded_texts

# 데이터 처리
if isinstance(data, list):  # JSON 데이터가 리스트인 경우
    for entry in data:
        conversation_id = entry.get("대화셋일련번호")  # 대화셋 일련번호 추출
        category = entry.get("카테고리", "기타")  # 카테고리 값 추출 (없으면 "기타")
        if conversation_id:
            for key in target_keys:
                value = entry.get(key)
                if value:  # 값이 있는 경우만 분석
                    # 형태소 분석 수행
                    analyzed = kiwi.analyze(value)

                    # 결과에서 어미와 조사 제외하고 어간만 추출
                    formatted_result = []
                    for sentence in analyzed:
                        for token in sentence[0]:
                            tag = token.tag
                            # 명사(NNG, NNP), 동사(VV), 형용사(VA)만 필터링
                            if tag in ['NNG', 'NNP', 'VV', 'VA']:
                                if tag in ['VV', 'VA']:  # 동사/형용사의 어간만 추가
                                    formatted_result.append(token.lemma)  # 어간 추출
                                else:
                                    formatted_result.append(token.form)  # 명사는 그대로 사용

                    # "원문", "형태소 분석 결과", "카테고리" 저장
                    analysis_results[conversation_id].append({
                        "원문": value,
                        "형태소 분석 결과": formatted_result,
                        "카테고리": category  # 카테고리 추가
                    })
else:
    print("JSON 데이터가 리스트 형식이 아닙니다.")

# 형태소 분석 후, 최대 길이에 맞춰 패딩 적용
all_analyzed_texts = []
for conversation_id, items in analysis_results.items():
    for item in items:
        all_analyzed_texts.append(" ".join(item["형태소 분석 결과"]))

# 최대 길이에 맞춰 패딩 처리
padded_texts = pad_text_to_max_length(all_analyzed_texts)

# 패딩된 형태소 분석 결과를 다시 저장
padded_index = 0
for conversation_id, items in analysis_results.items():
    for item in items:
        # 패딩된 텍스트를 할당
        item["패딩된 형태소 분석 결과"] = padded_texts[padded_index]
        padded_index += 1

# JSON으로 저장
output_path = r"C:\Users\Admin\Desktop\프로젝트_11월2차\Conversation_History_Analysis\data\output_with_padding_and_category.json"
with open(output_path, 'w', encoding='utf-8') as out_file:
    json.dump(analysis_results, out_file, ensure_ascii=False, indent=4)

print("분석 결과와 패딩, 카테고리가 저장되었습니다.")
