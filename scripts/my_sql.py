import pymysql as db
from datetime import datetime
import re

conn = db.connect(host= "192.168.101.213", user="jin", password='1234', db='conversation', charset='utf8')

cursor = conn.cursor()

# cursor.execute("use conversation")
# cursor.execute("select * from 상담이력;")
#
# print(cursor.fetchall())
# insert into 상담이력 values('서비스명', '통화시작', '통화종료', '통화시간', '고객명', '전화번호', '상담유형', '상담사', '상담내용')


def validation_data(data):
    def validate_datetime(date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False

    # 보조 함수: 전화번호 검증
    def validate_phone(phone):
        phone_regex = re.compile(r"^\d{2,4}-\d{3,4}-\d{4}$")  # 한국 전화번호 형식
        return bool(phone_regex.match(phone))

    # 보조 함수: 통화 시간 순서 검증
    def validate_time_order(start_time, end_time):
        start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        return end > start

    required_fields = {
        "서비스명": lambda x: isinstance(x, str) and 1 <= len(x) <= 255,
        "통화시작": lambda x: validate_datetime(x),
        "통화종료": lambda x: validate_datetime(x),
        "통화시간": lambda x: isinstance(x, int) and x > 0,
        "고객명": lambda x: isinstance(x, str) and 1 <= len(x) <= 100,
        "전화번호": lambda x: validate_phone(x),
        "상담유형": lambda x: isinstance(x, str) and 1 <= len(x) <= 50,
        "상담사": lambda x: isinstance(x, str) and 1 <= len(x) <= 100,
        "상담내용": lambda x: isinstance(x, str) and len(x) > 0,
    }

    # 필수 필드가 모두 있는지 확인
    for field in required_fields:
        if field not in data:
            print(f"필수 필드가 누락되었습니다: {field}")
            return False

        # 각 필드 값 검증
        if not required_fields[field](data[field]):
            print(f"유효하지 않은 값입니다: {field} ({data[field]})")
            return False

    # 통화 시작과 종료 시간 순서 검증
    if "통화시작" in data and "통화종료" in data:
        if not validate_time_order(data["통화시작"], data["통화종료"]):
            print("통화종료는 통화시작보다 나중이어야 합니다.")
            return False

    return True


def insert_data(data):
    if not validation_data(data):
        return

    try:
        with conn.cursor() as cur:
            query = "insert into 상담이력 (서비스명, 통화시작, 통화종료, 통화시간, 고객명, 전화번호, 상담유형, 상담사, 상담내용) values (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cur.execute("use conversation")

            cur.execute(query, (data['서비스명'],
                                data['통화시작'],
                                data['통화종료'],
                                data['통화시간'],
                                data['고객명'],
                                data['전화번호'],
                                data['상담유형'],
                                data['상담사'],
                                data['상담내용']
                                ))

            conn.commit()

    finally:
        conn.close()


temp_data = {
    "서비스명": "서비스A",
    "통화시작": "2024-11-19 10:00:00",  # 필드 누락
    "통화종료": "2024-11-19 10:30:00",
    "통화시간": 30,
    "고객명": "홍길동",
    "전화번호": "010-1234-5678",
    "상담유형": "기술지원",
    "상담사": "김상담사",
    "상담내용": "상담 내용입니다."
}

insert_data(temp_data)

cursor.execute("use conversation")
cursor.execute("select * from 상담이력;")

print(cursor.fetchall())