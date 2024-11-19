# import numpy as np
# from transformers import BertModel
# from keybert_test import extract_keywords
#
#
# def evaluate_model(predicted_keywords, true_keywords):
#     y_true = []
#     y_pred = []
#     print(predicted_keywords)
#     print(true_keywords)
#     for idx in range(len(predicted_keywords)):
#
#
#
# if __name__ == "__main__":
#     # 데이터 파일 경로
#     file_path = "../dataset/preprocessing/only_text_03.주문결제.json"
#
#     # KeyBERT 모델 초기화
#     bert_model = BertModel.from_pretrained('skt/kobert-base-v1')
#     predicted_keywords, df = extract_keywords(file_path, bert_model)
#
#     # 실제 정답 키워드 (샘플로 제공 필요)
#     # `true_keywords`는 사용자가 데이터에 따라 제공해야 합니다.
#     true_keywords = [
#         ['상품', '주문 결제'], ['배송', '환불'], ['제품', '구매'],  # ... (사용자 입력 필요)
#     ]
#
#     # 평가
#     mean_f1_score = evaluate_model(predicted_keywords, true_keywords)