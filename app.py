import time
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from flask_cors import CORS
import jwt
import datetime

# 비밀 키
SECRET_KEY = 'your_secret_key'

# Flask 애플리케이션 설정
app = Flask(
    __name__,
    static_folder="templates/dist",
    template_folder="templates/dist"
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:user_password@dbp_mysql_server/YMS_db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:1234@34.22.67.132/YMS_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)

# MySQL 연결 재시도 로직
connected = False
for attempt in range(5):
    try:
        with app.app_context():
            db.session.execute(text('SELECT 1'))
            connected = True
            print(f"MySQL 연결 성공! (시도 {attempt + 1}회)")
            break
    except OperationalError as e:
        print(f"MySQL 연결 대기 중... (시도 {attempt + 1}회, 오류: {str(e)})")
        time.sleep(5)

if not connected:
    print("MySQL에 연결할 수 없습니다. 데이터베이스 기능이 제한됩니다.")

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
    return render_template("index.html")


# 정적 파일 서빙
@app.route("/<path:path>")
def static_files(path):
    return app.send_static_file(path)


# 사용자 로그인 API
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        result = db.session.execute(text("""
            SELECT * 
            FROM Password 
            WHERE User_ID = :username AND Password = :password
        """), {"username": username, "password": password})
        user = result.fetchone()

        if user:
            role_query = "SELECT Role_ID FROM User WHERE User_ID = :username"
            role_result = db.session.execute(text(role_query), {"username": username})
            role = role_result.fetchone()

            if role:
                role_id = role._mapping['Role_ID']
                token = jwt.encode({
                    'user_id': user._mapping['User_ID'],
                    'role_id': role_id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }, SECRET_KEY, algorithm='HS256')

                return jsonify({
                    "success": True,
                    "message": "Login successful",
                    "role_id": role_id,
                    "token": token
                })
            else:
                return jsonify({"success": False, "message": "User role not found"}), 404
        else:
            return jsonify({"success": False, "message": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"success": False, "message": "An error occurred", "error": str(e)}), 500

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role_id = data.get('role_id')  # 클라이언트에서 전달한 Role ID

    if not username or not password or not role_id:
        return jsonify({"success": False, "message": "Invalid input"}), 400

    try:
        # User 테이블에 데이터 삽입
        print(f"Inserting into User: username={username}, role_id={role_id}")
        db.session.execute(text("""
            INSERT INTO User (User_ID, UserName, Role_ID)
            VALUES (:username, :username, :role_id)
        """), {"username": username, "role_id": role_id})

        # Password 테이블에 데이터 삽입
        print(f"Inserting into Password: username={username}")
        db.session.execute(text("""
            INSERT INTO Password (User_ID, Password)
            VALUES (:username, :password)
        """), {"username": username, "password": password})

        # 역할에 따라 Manager 또는 Driver 테이블에 데이터 삽입
        if role_id == 1:  # Manager
            print(f"Inserting into Manager: username={username}")
            db.session.execute(text("""
                INSERT INTO Manager (User_ID)
                VALUES (:username)
            """), {"username": username})

        elif role_id == 2:  # Driver
            print(f"Inserting into Driver: username={username}")
            db.session.execute(text("""
                INSERT INTO Driver (User_ID, Current_Status)
                VALUES (:username, 'Available')
            """), {"username": username})

        # 데이터베이스 커밋
        db.session.commit()
        print("Sign-up successful")
        return jsonify({"success": True, "message": "Sign-up successful"}), 201

    except Exception as e:
        # 에러 출력
        db.session.rollback()
        print(f"Error during sign-up: {e}")
        return jsonify({"success": False, "message": "An error occurred", "error": str(e)}), 500


# Transport_Log 데이터를 반환하는 API
@app.route('/api/transport_logs/get_logs', methods=['GET'])
def get_transport_logs():
    try:
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
                Depart_Date AS date,
                Log_Memo AS memo,
                Depart_Zone_ID AS departZone,
                Arrive_Zone_ID AS arriveZone                                                  
            FROM Transport_Log
        """))
        logs = [dict(row._mapping) for row in result]
        return jsonify({"success": True, "data": logs})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Driver 데이터 반환 API
@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    try:
        result = db.session.execute(text("""
            SELECT 
                d.User_ID AS id,
                u.UserName AS name,
                d.Current_Location AS current_location,
                d.Current_Status AS current_status,
                d.Private_Truck_Info AS private_truck_info,
                d.Truck_ID AS truck_id
            FROM Driver d
            INNER JOIN User u ON d.User_ID = u.User_ID
        """))
        drivers = [dict(row._mapping) for row in result]
        return jsonify({"success": True, "data": drivers})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# 특정 Yard 데이터 API
@app.route('/api/yard/<yard_id>', methods=['GET'])
def get_yard(yard_id):
    try:
        result = db.session.execute(text("""
            SELECT 
                Yard_ID AS id,
                Yard_Name AS name,
                Division_ID AS division_id,
                Address_ID AS address_id
            FROM Yard
            WHERE Yard_ID = :yard_id
        """), {"yard_id": yard_id})
        yard = result.fetchone()
        if yard:
            return jsonify({"success": True, "data": dict(yard._mapping)})
        else:
            return jsonify({"success": False, "message": "Yard not found."}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# 모든 Yard 데이터 반환 API
@app.route('/api/yard/all', methods=['GET'])
def get_all_yards():
    try:
        result = db.session.execute(text("""
            SELECT 
                Yard_ID AS id,
                Yard_Name AS name,
                Division_ID AS division_id,
                Address_ID AS address_id
            FROM Yard
        """))
        yards = [dict(row._mapping) for row in result]
        return jsonify({"success": True, "data": yards})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# 모든 Site 데이터 API
@app.route('/api/sites', methods=['GET'])
def get_sites():
    try:
        result = db.session.execute(text("""
            SELECT 
                Site_ID AS site_id,
                Yard_ID AS yard_id,
                Site_Name AS site_name,
                Storage_Type AS storage_type,
                Address_ID AS address_id,
                y_Cordinate AS y_coordinate,
                x_Cordinate AS x_coordinate,
                y_Max_Size AS y_max_size,
                x_Max_Size AS x_max_size
            FROM Site
        """))
        sites = [dict(row._mapping) for row in result]
        return jsonify({"success": True, "data": sites})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Zone 데이터를 반환하는 API
@app.route('/api/zones', methods=['GET'])
def get_zones():
    try:
        result = db.session.execute(text("""
            SELECT 
                Zone_ID AS zone_id,
                Site_ID AS site_id,
                Status AS status,
                y_Cordinate AS y_coordinate,
                x_Cordinate AS x_coordinate
            FROM Zone
        """))
        zones = [dict(row._mapping) for row in result]
        return jsonify({"success": True, "data": zones})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# 특정 Zone 데이터를 반환하는 API
@app.route('/api/zones/<zone_id>', methods=['GET'])
def get_zone(zone_id):
    try:
        result = db.session.execute(text("""
            SELECT 
                Zone_ID AS zone_id,
                Site_ID AS site_id,
                Status AS status,
                y_Cordinate AS y_coordinate,
                x_Cordinate AS x_coordinate
            FROM Zone
            WHERE Zone_ID = :zone_id
        """), {"zone_id": zone_id})
        zone = result.fetchone()
        if zone:
            return jsonify({"success": True, "data": dict(zone._mapping)})
        else:
            return jsonify({"success": False, "message": "Zone not found."}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# 특정 Yard에 속한 Zone 데이터를 반환하는 API
@app.route('/api/zones/by-yard/<yard_id>', methods=['GET'])
def get_zones_by_yard(yard_id):
    try:
        result = db.session.execute(text("""
            SELECT 
                z.Zone_ID AS zone_id,
                z.Site_ID AS site_id,
                z.Status AS status,
                z.y_Cordinate AS y_coordinate,
                z.x_Cordinate AS x_coordinate
            FROM Zone z
            INNER JOIN Site s ON z.Site_ID = s.Site_ID
            WHERE s.Yard_ID = :yard_id
        """), {"yard_id": yard_id})
        zones = [dict(row._mapping) for row in result]
        if zones:
            return jsonify({"success": True, "data": zones})
        else:
            return jsonify({"success": False, "message": f"No zones found for yard {yard_id}"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# 특정 Yard에 속한 Site 데이터를 반환하는 API
@app.route('/api/sites/by-yard/<yard_id>', methods=['GET'])
def get_sites_by_yard(yard_id):
    try:
        result = db.session.execute(text("""
            SELECT 
                Site_ID AS site_id,
                Site_Name AS site_name,
                Storage_Type AS storage_type,
                y_Cordinate AS y_coordinate,
                x_Cordinate AS x_coordinate,
                y_Max_Size AS y_max_size,
                x_Max_Size AS x_max_size
            FROM Site
            WHERE Yard_ID = :yard_id
        """), {"yard_id": yard_id})
        sites = [dict(row._mapping) for row in result]
        if sites:
            return jsonify({"success": True, "data": sites})
        else:
            return jsonify({"success": False, "message": f"No sites found for yard {yard_id}"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# 특정 Site에 속한 Zone 데이터를 반환하는 API
@app.route('/api/zones/by-site/<site_id>', methods=['GET'])
def get_zones_by_site(site_id):
    try:
        result = db.session.execute(text("""
            SELECT 
                Zone_ID AS zone_id,
                Status AS status,
                y_Cordinate AS y_coordinate,
                x_Cordinate AS x_coordinate
            FROM Zone
            WHERE Site_ID = :site_id
        """), {"site_id": site_id})
        zones = [dict(row._mapping) for row in result]
        if zones:
            return jsonify({"success": True, "data": zones})
        else:
            return jsonify({"success": False, "message": f"No zones found for site {site_id}"}), 404
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


@app.route('/api/transport_logs/assigned', methods=['GET'])
def get_assigned_transport_logs():
    try:
        result = db.session.execute(text("""
            SELECT 
                Log_ID AS id,
                Depart_Zone_ID AS depart_zone,
                Arrive_Zone_ID AS arrive_zone,
                Driver_ID AS driver_id,
                Assigned AS assigned,
                Depart_Date AS depart_date,
                Arrive_Date AS arrive_date
            FROM Transport_Log
            WHERE Assigned = TRUE
        """))
        logs = [dict(row._mapping) for row in result]
        return jsonify({"success": True, "data": logs})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Flask 애플리케이션 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
