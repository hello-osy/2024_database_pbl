# 베이스 이미지로 Python 사용
FROM python:3.8

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 파일 복사 및 설치
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Flask 애플리케이션 파일 복사
COPY . .

# Flask 애플리케이션 실행
CMD ["python", "app.py"]
