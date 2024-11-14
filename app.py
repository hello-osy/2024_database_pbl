import time
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:user_password@dbp_mysql_server/YMS_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# MySQL 연결 재시도 로직
connected = False
for _ in range(5):  # 최대 5회 재시도
    try:
        with app.app_context():
            db.session.execute(text('SELECT 1'))  # text()로 감싸기
            connected = True
            print("MySQL 연결 성공!")
            break
    except OperationalError:
        print("MySQL 연결 대기 중...")
        time.sleep(5)  # 5초 대기 후 재시도

if not connected:
    print("MySQL에 연결할 수 없습니다. 애플리케이션이 종료됩니다.")
    exit(1)  # MySQL에 연결할 수 없으면 애플리케이션 종료


# 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()

# 기본 URL: 연결 상태 확인
@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/test_db', endpoint='test_db')
def test_db_connection():
    try:
        # MySQL 서버에 간단한 쿼리 실행
        result = db.session.execute(text('SELECT 1'))
        result_list = [dict(row._mapping) for row in result]  # 각 행을 딕셔너리로 변환
        return jsonify({"status": "connected", "result": result_list})
    except Exception as e:
        return jsonify({"status": "not connected", "error": str(e)})


# /users URL: 직접 SQL 쿼리로 users 테이블 조회
@app.route('/users', endpoint='users')
def get_users():
    try:
        result = db.session.execute(text('SELECT * FROM User'))
        users = [dict(row._mapping) for row in result]
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# transport_log 엔드포인트 추가
@app.route('/transport_logs_page')
def transport_logs_page():
    return render_template('transport_logs.html')

@app.route('/transport_logs', endpoint='transport_logs')
def get_transport_logs():
    try:    
        result = db.session.execute(text('SELECT * FROM Transport_Log;'))
        transport_logs = [dict(row._mapping) for row in result]
        return jsonify(transport_logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
