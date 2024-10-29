import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql

# vercel에서 따로 환경 변수 추가해야함

app = Flask(__name__)
CORS(app)

# 환경 변수에서 MySQL 연결 정보 가져오기
# vercel 에서 환경변수 설정필요
db_config = {
    "host": os.getenv('MYSQL_HOST'),
    "user": os.getenv('MYSQL_USER'),
    "password": os.getenv('MYSQL_PASSWORD'),
    "database": os.getenv('MYSQL_DB')
}

# MySQL 연결 함수
def get_db_connection():
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# 기본 라우트
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return 'Hello, World!'
    if request.method == 'POST':
        # post 예제 코드
        # var calltest = new XMLHttpRequest; //객체 생성 
        # calltest.open("POST","http://localhost:8080/test.do",true);//요청 방식
        # calltest.setRequestHeader("Content-Type","application/json"); //헤더 정보 
        # calltest.send(JSON.stringify({"id":"kim123","date":"20220817"})); //param으로 json 데이터 전달. 
        return "Post"

# 예제 쿼리 라우트
@app.route('/about')
def about():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 'About' AS message")
            result = cursor.fetchone()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        connection.close()

# if __name__ == '__main__':
#     app.run(debug=True)