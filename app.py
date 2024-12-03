import time
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from flask_cors import CORS
import pymysql
import os
import jwt
import datetime


# 비밀 키
SECRET_KEY = 'your_secret_key'

# Flask 애플리케이션 설정
app = Flask(
    __name__,
    static_folder="templates/dist",  # 정적 파일 경로
    template_folder="templates/dist"  # 템플릿 파일 경로
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:1234@34.22.67.132/YMS_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)  # Cross-Origin Resource Sharing 활성화
db = SQLAlchemy(app)

# MySQL 연결 재시도 로직
connected = False
for attempt in range(5):  # 최대 5회 재시도
    try:
        with app.app_context():
            db.session.execute(text('SELECT 1'))  # 데이터베이스 연결 테스트
            connected = True
            print(f"MySQL 연결 성공! (시도 {attempt + 1}회)")
            break
    except OperationalError as e:
        print(f"MySQL 연결 대기 중... (시도 {attempt + 1}회, 오류: {str(e)})")
        time.sleep(5)  # 5초 대기 후 재시도

if not connected:
    print("MySQL에 연결할 수 없습니다. 계속 실행하지만 데이터베이스 기능은 제한됩니다.")

# 데이터베이스 테이블 생성
with app.app_context():
    try:
        db.create_all()
        print("데이터베이스 테이블 생성 완료!")
    except Exception as e:
        print(f"테이블 생성 실패: {str(e)}")

# 기본 라우트
@app.route("/")
def index():
    # Vue의 index.html 반환
    return render_template("index.html")

# 정적 파일 서빙 (css, js, img 등)
@app.route("/<path:path>")
def static_files(path):
    return app.send_static_file(path)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json  # 클라이언트에서 보낸 JSON 데이터
    username = data.get('username')
    password = data.get('password')

    try:
        # Password 테이블에서 User_ID와 Password를 확인
        result = db.session.execute(text(f"SELECT * FROM Password WHERE User_ID = :username AND Password = :password"),
                                    {"username": username, "password": password})
        user = result.fetchone()

        if user:
            # 해당 User_ID로 role_id를 조회
            query = "SELECT Role_ID FROM User WHERE User_ID = :username"
            result = db.session.execute(text(query), {"username": username})
            role = result.fetchone()

            if role:
                # dict로 변환하여 role_id 값을 가져옴
                role_id = role._mapping['Role_ID']  # role_id 가져오기

                # 실제 JWT 토큰 생성
                token = jwt.encode({
                    'user_id': user._mapping['User_ID'],
                    'role_id': role_id,  # role_id 반환
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 만료 시간 설정
                }, SECRET_KEY, algorithm='HS256')

                # 로그인 성공 시, JWT 토큰 반환
                return jsonify({
                    "success": True,
                    "message": "Login successful",
                    "role_id" : role_id,
                    "token": token  # 실제 생성된 JWT 토큰 반환
                })
            else:
                return jsonify({
                    "success": False,
                    "message": "User role not found"
                }), 404
        else:
            # 로그인 실패
            return jsonify({
                "success": False,
                "message": "Invalid username or password"
            }), 401
    except Exception as e:
        # 서버 에러 처리
        return jsonify({
            "success": False,
            "message": "An error occurred",
            "error": str(e)
        }), 500

# Transport_Log 데이터를 반환하는 API
@app.route('/api/transport_logs', methods=['GET'])
def get_transport_logs():
    try:
        # Transport_Log 테이블 데이터 가져오기
        result = db.session.execute(text("""
            SELECT 
                Log_ID AS id,
                Driver_ID AS driver,
                Truck_ID AS vehicle,
                CASE 
                    WHEN CURDATE() BETWEEN Depart_Date AND Arrive_Date THEN 'In Progress'
                    WHEN CURDATE() > Arrive_Date THEN 'Completed'
                    ELSE 'Scheduled'
                END AS status,
                DATEDIFF(Arrive_Date, Depart_Date) * 50 AS distance, -- 임의 거리 계산
                Depart_Date AS date
            FROM Transport_Log
        """))
        
        # 결과를 JSON으로 변환
        logs = [dict(row._mapping) for row in result]
        return jsonify({"success": True, "data": logs})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# 데이터베이스 연결 테스트 API
@app.route("/test_db", methods=["GET"])
def test_db_connection():
    try:
        result = db.session.execute(text('SELECT 1'))
        return jsonify({"status": "connected", "result": [dict(row._mapping) for row in result]})
    except Exception as e:
        return jsonify({"status": "not connected", "error": str(e)}), 500

# Flask 애플리케이션 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
