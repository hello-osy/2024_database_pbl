import time
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from flask_cors import CORS
import jwt
from sqlalchemy.exc import SQLAlchemyError
# import datetime
from datetime import datetime, timedelta


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

@app.route('/api/transport_logs/release/<int:log_id>', methods=['POST'])
def release_transport_log(log_id):
    try:
        # 운송 로그 조회
        result = db.session.execute(text("""
            SELECT 
                Truck_ID, Chassis_ID, Container_ID, Trailer_ID 
            FROM Transport_Log 
            WHERE Log_ID = :log_id AND Assigned = 0
        """), {"log_id": log_id}).fetchone()

        if not result:
            return jsonify({"success": False, "message": f"Log ID {log_id} not found or already released"}), 404

        # 할당 해제 (Assigned 상태 업데이트)
        db.session.execute(text("""
            UPDATE Transport_Log
            SET Assigned = -1
            WHERE Log_ID = :log_id
        """), {"log_id": log_id})

        # 각 장비의 상태 업데이트
        if result.Truck_ID:
            db.session.execute(text("""
                UPDATE Truck
                SET Status = 'Available'
                WHERE Truck_ID = :truck_id
            """), {"truck_id": result.Truck_ID})

        if result.Chassis_ID:
            db.session.execute(text("""
                UPDATE Chassis
                SET Status = 'Available'
                WHERE Chassis_ID = :chassis_id
            """), {"chassis_id": result.Chassis_ID})

        if result.Container_ID:
            db.session.execute(text("""
                UPDATE Container
                SET Status = 'Available'
                WHERE Container_ID = :container_id
            """), {"container_id": result.Container_ID})

        if result.Trailer_ID:
            db.session.execute(text("""
                UPDATE Trailer
                SET Status = 'Available'
                WHERE Trailer_ID = :trailer_id
            """), {"trailer_id": result.Trailer_ID})

        db.session.commit()
        return jsonify({"success": True, "message": f"Log {log_id} released and equipment status updated"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "An error occurred while releasing the log", "error": str(e)}), 500

@app.route('/api/equipment/available', methods=['PUT'])
def update_equipment_status():
    try:
        # 요청 데이터
        data = request.json
        equipment_id = data.get('id')

        if not equipment_id:
            return jsonify({"success": False, "message": "Equipment ID is required"}), 400

        # 트럭, 샤시, 컨테이너, 트레일러 테이블을 순차적으로 확인
        queries = {
            "Truck": "UPDATE Truck SET Status='Available' WHERE Truck_ID=:equipment_id",
            "Chassis": "UPDATE Chassis SET Status='Available' WHERE Chassis_ID=:equipment_id",
            "Container": "UPDATE Container SET Status='Available' WHERE Container_ID=:equipment_id",
            "Trailer": "UPDATE Trailer SET Status='Available' WHERE Trailer_ID=:equipment_id",
        }

        success = False

        for table, query in queries.items():
            result = db.session.execute(text(query), {"equipment_id": equipment_id})
            if result.rowcount > 0:
                success = True
                break

        if not success:
            return jsonify({"success": False, "message": f"Equipment {equipment_id} not found"}), 404

        db.session.commit()
        return jsonify({"success": True, "message": f"Equipment {equipment_id} updated to 'Available'"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "An error occurred while updating equipment status", "error": str(e)}), 500

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
                    'exp': datetime.utcnow() + timedelta(hours=1)
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

@app.route('/api/driver-info', methods=['GET'])
def get_driver_info():
    print("Driver info API called")  # API 호출 로그
    auth_header = request.headers.get('Authorization')
    print(f"Authorization Header: {auth_header}")  # Authorization 헤더 값 출력

    # Authorization 헤더 유효성 확인
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"success": False, "message": "Authorization header missing or invalid"}), 401

    # 토큰 추출
    token = auth_header.split(" ")[1]
    try:
        # JWT 디코딩
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(f"Decoded Payload: {payload}")  # 디코딩된 페이로드 출력

        # DB 쿼리 실행
        user_id = payload['user_id']
        result = db.session.execute(text("""
            SELECT 
                d.User_ID, 
                d.Current_Status, 
                d.Current_Location, 
                d.Private_Truck_Info, 
                d.Truck_ID,
                d.Trips_Completed,
                d.Monthly_Earnings,
                d.Average_Ratings,
                u.UserName,
                u.Email,
                u.Phone_Number
            FROM Driver d
            JOIN User u ON d.User_ID = u.User_ID
            WHERE d.User_ID = :user_id
        """), {"user_id": user_id})
        driver = result.fetchone()

        if driver:
            print(f"Driver found: {driver}")  # 드라이버 정보 출력
            return jsonify({
                "success": True,
                "driver": {
                    "user_id": driver._mapping['User_ID'],
                    "name": driver._mapping['UserName'],
                    "email": driver._mapping['Email'],
                    "phone": driver._mapping['Phone_Number'],
                    "status": driver._mapping['Current_Status'],
                    "location": driver._mapping['Current_Location'],
                    "truck_info": driver._mapping['Private_Truck_Info'],
                    "truck_id": driver._mapping['Truck_ID'],
                    "tripsCompleted": driver._mapping['Trips_Completed'],
                    "monthlyEarnings": driver._mapping['Monthly_Earnings'],
                    "averageRatings": driver._mapping['Average_Ratings']
                }
            })
        else:
            print("Driver not found")  # 드라이버 없음 로그
            return jsonify({"success": False, "message": "Driver not found"}), 404

    except jwt.ExpiredSignatureError:
        print("Token has expired")  # 토큰 만료 로그
        return jsonify({"success": False, "message": "Token expired"}), 401
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")  # 잘못된 토큰 로그
        return jsonify({"success": False, "message": "Invalid token"}), 401
    except Exception as e:
        print(f"An error occurred: {e}")  # 서버 에러 로그
        return jsonify({"success": False, "message": "An error occurred", "error": str(e)}), 500

# JWT 토큰 디코딩 함수
def get_user_id_from_token(auth_header):
    try:
        # Authorization 헤더가 비어있거나 잘못된 형식일 경우 처리
        if not auth_header or not auth_header.startswith("Bearer "):
            raise ValueError("Invalid Authorization header")
        
        # "Bearer " 이후의 토큰 부분만 추출
        token = auth_header.split(" ")[1]
        
        # JWT 디코딩
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        # `user_id` 추출
        user_id = payload.get("user_id")
        if not user_id:
            raise ValueError("user_id not found in token")
        
        return user_id
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
    except Exception as e:
        raise ValueError(f"Error decoding token: {str(e)}")
    
@app.route('/api/update-status', methods=['POST'])
def update_status():
    # Authorization 헤더에서 토큰 추출
    auth_header = request.headers.get('Authorization')
    try:
        # 토큰에서 user_id 추출
        user_id = get_user_id_from_token(auth_header)
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 401

    # 요청 데이터에서 status 값 가져오기
    data = request.json
    new_status = data.get('status')
    valid_statuses = ['Available', 'On a Trip', 'Offline']

    if not new_status:
        return jsonify({"success": False, "message": "Status is missing"}), 400
    if new_status not in valid_statuses:
        return jsonify({"success": False, "message": f"Invalid status value. Must be one of {valid_statuses}"}), 400

    # DB 업데이트
    try:
        db.session.execute(text("""
            UPDATE Driver
            SET Current_Status = :new_status
            WHERE User_ID = :user_id
        """), {"new_status": new_status, "user_id": user_id})
        db.session.commit()
        return jsonify({"success": True, "message": "Status updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": "An error occurred", "error": str(e)}), 500

@app.route('/api/update-profile', methods=['POST'])
def update_profile():
    try:
        # Authorization 헤더에서 토큰 추출
        auth_header = request.headers.get('Authorization')
        user_id = get_user_id_from_token(auth_header)

        # 클라이언트로부터 데이터 받기
        data = request.json
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        private_truck_info = data.get('privateTruckInfo')
        password = data.get('password')  # 비밀번호 변경이 필요한 경우

        # 각 필드 업데이트 처리
        if email:
            print(f"Updating email to: {email}")  # 디버깅 로그
            db.session.execute(text("""
                UPDATE User
                SET Email = :email
                WHERE User_ID = :user_id
            """), {"email": email, "user_id": user_id})

        if phone:
            print(f"Updating phone to: {phone}")  # 디버깅 로그
            db.session.execute(text("""
                UPDATE User
                SET Phone_Number = :phone
                WHERE User_ID = :user_id
            """), {"phone": phone, "user_id": user_id})

        if address:
            print(f"Updating address to: {address}")  # 디버깅 로그
            db.session.execute(text("""
                UPDATE Driver
                SET Current_Location = :address
                WHERE User_ID = :user_id
            """), {"address": address, "user_id": user_id})

        if private_truck_info:
            print(f"Updating private_truck_info to: {private_truck_info}")  # 디버깅 로그
            db.session.execute(text("""
                UPDATE Driver
                SET Private_Truck_Info = :private_truck_info
                WHERE User_ID = :user_id
            """), {"private_truck_info": private_truck_info, "user_id": user_id})

        if password:
            print(f"Updating password")  # 디버깅 로그
            db.session.execute(text("""
                UPDATE Password
                SET Password = :password
                WHERE User_ID = :user_id
            """), {"password": password, "user_id": user_id})

        db.session.commit()
        print("Profile updated successfully")  # 디버깅 로그
        return jsonify({"success": True, "message": "Profile updated successfully"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "An error occurred", "error": str(e)}), 500
    
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    print("Recieved full request data: ", data) # Debug
    
    username = data.get('username')
    password = data.get('password')
    role_id = data.get('role_id')  # 클라이언트에서 전달한 Role ID
    driver_phone = data.get('driver_phone')

    if not username or not password or not role_id:
        return jsonify({"success": False, "message": "Invalid input"}), 400

    try:
        # User 테이블에 데이터 삽입
        print(f"Inserting into User: username={username}, role_id={role_id}")
        db.session.execute(text("""
            INSERT INTO User (User_ID, UserName, Role_ID, Phone_Number)
            VALUES (:username, :username, :role_id, :driver_phone)
        """), {
            "username": username,
            "role_id": role_id,
            "driver_phone": driver_phone
        })

        # Password 테이블에 데이터 삽입
        print(f"Inserting into Password: username={username}")
        db.session.execute(text("""
            INSERT INTO Password (User_ID, Password)
            VALUES (:username, :password)
        """), {"username": username, "password": password})

        # 역할에 따라 Manager 또는 Driver 테이블에 데이터 삽입
        if role_id == '1':  # Manager
            print(f"Inserting into Manager: username={username}")
            db.session.execute(text("""
                INSERT INTO Manager (User_ID)
                VALUES (:username)
            """), {"username": username})

        elif role_id == '2':  # Driver
            division = data.get('division')
            truck_info = data.get('truck_info')

            # Debug prints
            print("Received division value:", division)
            print("Received truck_info value:", truck_info)

             # Validation
            if not division:
                return jsonify({"success": False, "message": "Division is required"}), 400
            if not truck_info:
                return jsonify({"success": False, "message": "Truck info is required"}), 400

            # division 값을 division 이름으로 반환
            division_map = {
                '1': 'LA',
                '2': 'PHX',
                '3': 'HOU',
                '4': 'MOB',
                '5': 'SAV'
            }
            
            # 트럭 값을 개인 여부로 반환
            truck_info_map = {
                '1': 'Private Truck',
                '2': 'Company Truck'  
            }
            
            current_location = division_map.get(division)
            private_truck_info = truck_info_map.get(truck_info)
            
             # Debug prints for mapped values
            print("Mapped location:", current_location)
            print("Mapped truck info:", private_truck_info)
            
            print(f"Inserting into Driver: username={username}")
            db.session.execute(text("""
                INSERT INTO Driver (User_ID, Current_Location, Private_Truck_Info)
                VALUES (:username, :current_location, :private_truck_info)
            """), {
                "username": username,
                "current_location": current_location,
                "private_truck_info": private_truck_info
            })

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
                    WHEN Assigned = 0 THEN 'Reserved'
                    WHEN Assigned = 1 THEN 'Delivering'
                    WHEN Assigned = -1 THEN 'Rejected'
                    WHEN Assigned = 2 THEN 'Completed'
                    ELSE 'Unknown'
                END AS status,
                Depart_Date AS departDate,
                Arrive_Date AS arriveDate,
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

# LA Division 데이터 API
@app.route('/api/yard/la', methods=['GET'])
def get_la_yards():
    try:
        result = db.session.execute(text("""
            SELECT
                Yard_ID AS id,
                Yard_Name AS name,
                Division_ID AS division_id,
                Address_ID AS address_id
            FROM Yard
            WHERE Division_ID = 'LA'
        """))
        yards = [dict(row._mapping) for row in result]
        return jsonify({"success": True, "data": yards})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
        
# PHX Division 데이터 API
@app.route('/api/yard/phx', methods=['GET'])
def get_phx_yards():
    try:
        result = db.session.execute(text("""
            SELECT
                Yard_ID AS id,
                Yard_Name AS name,
                Division_ID AS division_id,
                Address_ID AS address_id
            FROM Yard
            WHERE Division_ID = 'PHX'
        """))
        yards = [dict(row._mapping) for row in result]
        return jsonify({"success": True, "data": yards})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# HOU Division 데이터 API
@app.route('/api/yard/hou', methods=['GET'])
def get_hou_yards():
    try:
        result = db.session.execute(text("""
            SELECT
                Yard_ID AS id,
                Yard_Name AS name,
                Division_ID AS division_id,
                Address_ID AS address_id
            FROM Yard
            WHERE Division_ID = 'HOU'
        """))
        yards = [dict(row._mapping) for row in result]
        return jsonify({"success": True, "data": yards})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# MOB Division 데이터 API
@app.route('/api/yard/mob', methods=['GET'])
def get_mob_yards():
    try:
        result = db.session.execute(text("""
            SELECT
                Yard_ID AS id,
                Yard_Name AS name,
                Division_ID AS division_id,
                Address_ID AS address_id
            FROM Yard
            WHERE Division_ID = 'MOB'
        """))
        yards = [dict(row._mapping) for row in result]
        return jsonify({"success": True, "data": yards})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
# SAV Division 데이터 API
@app.route('/api/yard/sav', methods=['GET'])
def get_sav_yards():
    try:
        result = db.session.execute(text("""
            SELECT
                Yard_ID AS id,
                Yard_Name AS name,
                Division_ID AS division_id,
                Address_ID AS address_id
            FROM Yard
            WHERE Division_ID = 'SAV'
        """))
        yards = [dict(row._mapping) for row in result]
        return jsonify({"success": True, "data": yards})
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
            WHERE Assigned = 0;
        """))
        logs = [dict(row._mapping) for row in result]
        return jsonify({"success": True, "data": logs})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/update-transport-log', methods=['POST'])
def update_transport_log():
    # Authorization 헤더에서 토큰 추출
    auth_header = request.headers.get('Authorization')
    try:
        # 토큰에서 user_id 추출
        user_id = get_user_id_from_token(auth_header)
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 401

    # 요청 데이터에서 log_id와 상태 값 가져오기
    data = request.json
    log_id = data.get('log_id')
    assigned = data.get('assigned')  # Assigned 값: 0, 1, -1, 2
    completed = data.get('completed', False)  # 완료 여부 (기본값 False)

    if not log_id:
        return jsonify({"success": False, "message": "Log ID is required"}), 400

    try:
        if assigned == -1:
            # 거부된 경우
            db.session.execute(text("""
                UPDATE Transport_Log
                SET Assigned = -1
                WHERE Log_ID = :log_id AND Driver_ID = :user_id
            """), {"log_id": log_id, "user_id": user_id})
        elif completed:
            # 완료된 경우
            db.session.execute(text("""
                UPDATE Transport_Log
                SET Assigned = 2, Log_Memo = 'Completed'
                WHERE Log_ID = :log_id AND Driver_ID = :user_id
            """), {"log_id": log_id, "user_id": user_id})
        else:
            # 수락된 경우
            db.session.execute(text("""
                UPDATE Transport_Log
                SET Assigned = :assigned
                WHERE Log_ID = :log_id AND Driver_ID = :user_id
            """), {"assigned": assigned, "log_id": log_id, "user_id": user_id})

        db.session.commit()
        return jsonify({"success": True, "message": "Transport log updated successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "An error occurred", "error": str(e)}), 500

@app.route('/api/transport_logs/get_logs_by_driver', methods=['GET'])
def get_transport_logs_by_driver():
    try:
        auth_header = request.headers.get('Authorization')
        print(f"Authorization Header: {auth_header}")  # 디버깅 로그
        user_id = get_user_id_from_token(auth_header)
        print(f"User ID Decoded: {user_id}")  # 디코딩된 user_id 확인

        result = db.session.execute(text("""
            SELECT 
                Log_ID AS id,
                Driver_ID AS driver_id,
                Depart_Zone_ID AS departZone,
                Arrive_Zone_ID AS arriveZone,
                Depart_Date AS departDate,
                Arrive_Date AS arriveDate,
                Assigned AS assigned,
                Log_Memo AS memo
            FROM Transport_Log
            WHERE Driver_ID = :user_id AND Assigned != -1  -- 거부된 항목 제외
        """), {"user_id": user_id})

        logs = [dict(row._mapping) for row in result]
        print(f"Logs Retrieved: {logs}")  # 로그 출력
        return jsonify({"success": True, "data": logs})
    except ValueError as ve:
        print(f"ValueError: {str(ve)}")  # 디버깅 로그
        return jsonify({"success": False, "message": str(ve)}), 401
    except Exception as e:
        print(f"Exception: {str(e)}")  # 디버깅 로그
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/yard/stats', methods=['GET'])
def get_yard_stats():
    # URL에서 yard_id 가져오기
    yard_id = request.args.get('yard_id')
    
    if not yard_id:
        return jsonify({"success": False, "message": "yard_id is required"}), 400

    try:
        # Truck 갯수 쿼리
        truck_count_query = """
            select count(Truck_ID) from Truck where Zone_ID in (select Zone_ID from Zone where Site_ID in (select Site_ID from Site where Yard_ID=:yard_id and Storage_Type='Truck'));
        """
        truck_result = db.session.execute(text(truck_count_query), {"yard_id": yard_id})
        truck_count = truck_result.scalar()  # 단일 값 가져오기

        # Chassis 갯수 쿼리
        chassis_count_query = """
            select count(Chassis_ID) from Chassis where Zone_ID in (select Zone_ID from Zone where Site_ID in (select Site_ID from Site where Yard_ID=:yard_id and Storage_Type='Chassis'));
        """
        chassis_result = db.session.execute(text(chassis_count_query), {"yard_id": yard_id})
        chassis_count = chassis_result.scalar()

        # Container 갯수 쿼리
        container_count_query = """
            select count(Container_ID) from Container where Zone_ID in (select Zone_ID from Zone where Site_ID in (select Site_ID from Site where Yard_ID=:yard_id and Storage_Type='Container'));
        """
        container_result = db.session.execute(text(container_count_query), {"yard_id": yard_id})
        container_count = container_result.scalar()

        # Trailer 갯수 쿼리
        trailer_count_query = """
            select count(Trailer_ID) from Trailer where Zone_ID in (select Zone_ID from Zone where Site_ID in (select Site_ID from Site where Yard_ID=:yard_id and Storage_Type='Trailer'));
        """
        trailer_result = db.session.execute(text(trailer_count_query), {"yard_id": yard_id})
        trailer_count = trailer_result.scalar()

        # 결과 반환
        return jsonify({
            "success": True,
            "data": {
                "total_trucks": truck_count,
                "total_chassis": chassis_count,
                "total_containers": container_count,
                "total_trailers": trailer_count,
            }
        })

    except Exception as e:
        return jsonify({"success": False, "message": "An error occurred", "error": str(e)}), 500


@app.route('/api/driver/stats', methods=['GET'])
def get_driver_stats():
    # URL에서 yard_id 가져오기
    yard_id = request.args.get('yard_id')
    
    if not yard_id:
        return jsonify({"success": False, "message": "yard_id is required"}), 400

    try:
        # SQL 쿼리 실행
        query = """
        SELECT User_ID, Current_Location, Current_Status
        FROM Driver 
        WHERE Current_Location IN (
            SELECT Division_ID FROM Yard WHERE Yard_ID = :yard_id
        );
        """
        query_result = db.session.execute(text(query), {"yard_id": yard_id}).fetchall()

        # 튜플의 인덱스로 접근
        drivers = [
            {
                "User_ID": row[0],  # 첫 번째 컬럼
                "Current_Location": row[1],  # 두 번째 컬럼
                "Current_Status": row[2]  # 세 번째 컬럼
            }
            for row in query_result
        ]

        # JSON 형태로 응답
        return jsonify({
            "success": True,
            "data": drivers
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "An error occurred",
            "error": str(e)
        }), 500



@app.route('/api/yard/siteStatus', methods=['GET'])
def get_site_status():
    yard_id = request.args.get('yard_id')

    if not yard_id:
        return jsonify({"success": False, "message": "yard_id is required"}), 400

    try:
        # Truck 데이터 가져오기
        truck_query = """
        select Truck_ID AS id, Status AS status from Truck where Zone_ID in (select Zone_ID from Zone where Site_ID in (select Site_ID from Site where Yard_ID=:yard_id and Storage_Type='Truck'));
        """
        truck_result = db.session.execute(text(truck_query), {"yard_id": yard_id}).fetchall()

        # Chassis 데이터 가져오기
        chassis_query = """
        select Chassis_ID AS id, Status AS status from Chassis where Zone_ID in (select Zone_ID from Zone where Site_ID in (select Site_ID from Site where Yard_ID=:yard_id and Storage_Type='Chassis'));
        """
        chassis_result = db.session.execute(text(chassis_query), {"yard_id": yard_id}).fetchall()

        # Container 데이터 가져오기
        container_query = """
        select Container_ID AS id, Status AS status from Container where Zone_ID in (select Zone_ID from Zone where Site_ID in (select Site_ID from Site where Yard_ID=:yard_id and Storage_Type='Container'));
        """
        container_result = db.session.execute(text(container_query), {"yard_id": yard_id}).fetchall()

        # Trailer 데이터 가져오기
        trailer_query = """
        select Trailer_ID AS id, Status AS status from Trailer where Zone_ID in (select Zone_ID from Zone where Site_ID in (select Site_ID from Site where Yard_ID=:yard_id and Storage_Type='Trailer'));
        """
        trailer_result = db.session.execute(text(trailer_query), {"yard_id": yard_id}).fetchall()

        # 데이터를 사이트별로 그룹화
        sites = {
            "Truck Site": {"name": "Truck Site", "equipments": {"Truck": [], "Chassis": [], "Container": [], "Trailer": []}},
            "Chassis Site": {"name": "Chassis Site", "equipments": {"Truck": [], "Chassis": [], "Container": [], "Trailer": []}},
            "Container Site": {"name": "Container Site", "equipments": {"Truck": [], "Chassis": [], "Container": [], "Trailer": []}},
            "Trailer Site": {"name": "Trailer Site", "equipments": {"Truck": [], "Chassis": [], "Container": [], "Trailer": []}},
        }

        # Truck 데이터 추가
        for row in truck_result:
            sites["Truck Site"]["equipments"]["Truck"].append({"id": row[0], "status": row[1]})

        # Chassis 데이터 추가
        for row in chassis_result:
            sites["Chassis Site"]["equipments"]["Chassis"].append({"id": row[0], "status": row[1]})

        # Container 데이터 추가
        for row in container_result:
            sites["Container Site"]["equipments"]["Container"].append({"id": row[0], "status": row[1]})

        # Trailer 데이터 추가
        for row in trailer_result:
            sites["Trailer Site"]["equipments"]["Trailer"].append({"id": row[0], "status": row[1]})

        # JSON 응답
        return jsonify({"success": True, "data": list(sites.values())})

    except Exception as e:
        return jsonify({"success": False, "message": "An error occurred", "error": str(e)}), 500

@app.route('/api/transport_logs/all', methods=['GET'])
def get_all_transport_logs():
    try:
        # Transport_Log 테이블의 모든 데이터를 가져옴
        result = db.session.execute(text("SELECT * FROM Transport_Log"))
        logs = [dict(row._mapping) for row in result]
        return jsonify({"success": True, "data": logs})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/get/availableZones', methods=['GET'])
def get_available_zones():
    try:
        result = db.session.execute(text("""
            SELECT Zone_ID AS id
            FROM Zone
        """)).fetchall()

        # _mapping 사용
        zones = [row._mapping['id'] for row in result]

        return jsonify({"success": True, "data": zones})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500




@app.route('/api/transport-log', methods=['POST'])
def register_transport_log():
    data = request.json

    # 필수 필드 검증
    required_fields = ["truck", "arriveDate", "arriveZone", "driver"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400

    # 날짜 형식 검증
    try:
        arrive_date = datetime.strptime(data["arriveDate"], "%Y-%m-%d")
    except ValueError:
        return jsonify({"success": False, "message": "Invalid date format. Expected YYYY-MM-DD."}), 400

    # 트레일러와 샤시/컨테이너 중 하나만 있어야 함
    if data.get("trailer") and (data.get("chassis") or data.get("container")):
        return jsonify({"success": False, "message": "Cannot have both trailer and chassis/container."}), 400

    # 입력 데이터 처리
    truck_id = data["truck"]["id"]
    chassis_id = data.get("chassis", {}).get("id") if data.get("chassis") else None
    container_id = data.get("container", {}).get("id") if data.get("container") else None
    trailer_id = data.get("trailer", {}).get("id") if data.get("trailer") else None
    arrive_zone = data["arriveZone"]
    driver_id = data["driver"]

    # Assigned 필드 기본값 설정
    assigned = 0

    # 현재 날짜를 Depart_Date로 설정
    depart_date = datetime.now()

    # Truck_ID를 이용하여 Depart_Zone_ID 조회
    try:
        result = db.session.execute(
            text("SELECT Zone_ID FROM Truck WHERE Truck_ID = :truck_id"),
            {"truck_id": truck_id}
        )
        depart_zone_id = result.scalar()  # Zone_ID를 가져옴

        if not depart_zone_id:
            return jsonify({"success": False, "message": "Depart Zone ID not found for the given Truck ID."}), 400
    except Exception as e:
        return jsonify({"success": False, "message": "Error retrieving Depart Zone ID.", "error": str(e)}), 500

    try:
        query = """
        INSERT INTO Transport_Log (
            Driver_ID, Container_ID, Chassis_ID, Truck_ID, Trailer_ID,
            Depart_Zone_ID, Depart_Date, Arrive_Zone_ID, Arrive_Date, Assigned
        )
        VALUES (
            :driver_id, :container_id, :chassis_id, :truck_id, :trailer_id,
            :depart_zone_id, :depart_date, :arrive_zone, :arrive_date, :assigned
        )
        """

        db.session.execute(
            text(query),
            {
                "driver_id": driver_id,
                "container_id": container_id,
                "chassis_id": chassis_id,
                "truck_id": truck_id,
                "trailer_id": trailer_id,
                "depart_zone_id": depart_zone_id,
                "depart_date": depart_date,
                "arrive_zone": arrive_zone,
                "arrive_date": arrive_date,
                "assigned": assigned,
            }
        )

        db.session.commit()

        # 장비 : Truck, Chassis, Container, Trailer
        # 장비를 Reserved로 status 변환 필요
        if truck_id is not None:
            query = """
            UPDATE Truck
            SET Status = 'Reserved'
            WHERE Truck_ID=:truck_id;
            """
            db.session.execute(text(query),{"truck_id": truck_id})
            db.session.commit()

        if chassis_id is not None:
            query = """
            UPDATE Chassis
            SET Status = 'Reserved'
            WHERE Chassis_ID=:chassis_id;
            """
            db.session.execute(text(query),{"chassis_id": chassis_id})
            db.session.commit()

            
        if container_id is not None:
            query = """
            UPDATE Container
            SET Status = 'Reserved'
            WHERE Container_ID=:container_id;
            """
            db.session.execute(text(query),{"container_id": container_id})
            db.session.commit()

            
        if trailer_id is not None:
            query = """
            UPDATE Trailer
            SET Status = 'Reserved'
            WHERE Trailer_ID=:trailer_id;
            """
            db.session.execute(text(query),{"trailer_id": trailer_id})
            db.session.commit()
            
        return jsonify({"success": True, "message": "Transport log registered successfully!"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Failed to register transport log", "error": str(e)}), 500


@app.route('/api/transport_logs/update_memo', methods=['POST'])
def update_transport_log_memo():
    try:
        # 요청에서 데이터 추출
        data = request.json
        log_id = data.get("log_id")
        log_memo = data.get("log_memo")
        assigned = data.get('assigned', 2)

        # 데이터베이스 업데이트
        query = text("""
            UPDATE Transport_Log
            SET Log_Memo = :log_memo, Assigned = :assigned
            WHERE Log_ID = :log_id;
        """)
        db.session.execute(query, {'log_memo': log_memo, 'assigned': assigned, 'log_id': log_id})
        db.session.commit()

        return jsonify({"success": True, "message": "Log memo updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/get/currentZones", methods=["POST"])
def get_current_zones():
    """
    API Endpoint to fetch current zones based on yard_id and equipment type.
    """
    try:
        # 요청 데이터 받기
        data = request.get_json()
        yard_id = data.get("id")
        equipment_type = data.get("type").lower()  # truck, chassis, container, trailer

        if not yard_id or not equipment_type:
            return jsonify({"success": False, "message": "Missing yard_id or equipment type"}), 400

        # 장비 타입에 따라 테이블 및 필드 매핑
        table_mapping = {
            "truck": "Truck",
            "chassis": "Chassis",
            "container": "Container",
            "trailer": "Trailer"
        }

        if equipment_type not in table_mapping:
            return jsonify({"success": False, "message": f"Invalid equipment type: {equipment_type}"}), 400

        type = table_mapping[equipment_type]

        # SQL 쿼리 실행
        query = f"""
        SELECT Zone_ID AS id
        FROM Zone
        where Site_ID in (select Site_ID from Site where Yard_ID=:yard_id and Storage_Type=:truck_id) and Status<>'In Use';
        """
        # select * from Zone where Site_ID in (select Site_ID from Site where Yard_ID='HOU_YARD_0001' and Storage_Type='Container') and Status<>'In Use'
        result = db.session.execute(text(query), {"yard_id": yard_id, "truck_id":type}).fetchall()

        # 결과 반환
        zones = [{"id": row[0]} for row in result]  # row[0]으로 접근
        return jsonify({"success": True, "data": zones}), 200

    except Exception as e:
        return jsonify({"success": False, "message": "Error retrieving zones", "error": str(e)}), 500


@app.route("/api/equipment/add", methods=["POST"])
def add_equipment():
    """
    API Endpoint to add equipment to a zone.
    """
    try:
        # 요청 데이터 확인
        data = request.get_json()
        equipment_id = data.get("id")
        zone_id = data.get("zone")
        equipment_type = data.get("type").lower()
        yard_id = data.get("yard_id")

        if not all([equipment_id, zone_id, equipment_type, yard_id]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # 테이블 매핑
        table_mapping = {
            "truck": "Truck",
            "chassis": "Chassis",
            "container": "Container",
            "trailer": "Trailer",
        }

        if equipment_type not in table_mapping:
            return jsonify({"success": False, "message": f"Invalid equipment type: {equipment_type}"}), 400

        # 장비 삽입
        query = f"""
        INSERT INTO {table_mapping[equipment_type]} ({table_mapping[equipment_type]}_ID, Zone_ID, Status)
        VALUES (:equipment_id, :zone_id, 'Available')
        """
        print(f"query : {query}")
        db.session.execute(
            text(query),
            {"equipment_id": equipment_id, "zone_id": zone_id},
        )
        db.session.commit()

        
        #  # 장비 삽입
        # query = f"""
        # INSERT INTO {table_mapping[equipment_type]} ({table_mapping[equipment_type]}_ID, Zone_ID, Status)
        # VALUES (:equipment_id, :zone_id, 'Available')
        # """
        # db.session.execute(
        #     text(query),
        #     {"equipment_id": equipment_id, "zone_id": zone_id},
        # )
        # db.session.commit()


        return jsonify({"success": True, "message": f"{equipment_type.capitalize()} added successfully!"}), 201

    except Exception as e:
        return jsonify({"success": False, "message": "Error adding equipment", "error": str(e)}), 500


@app.route("/api/equipment/delete", methods=["POST"])
def delete_equipment():
    """
    API Endpoint to delete equipment from a zone.
    """
    try:
        # 요청 데이터 받기
        data = request.get_json()
        equipment_id = data.get("id")
        equipment_type = data.get("type").lower()[:-5]  # truck, chassis, container, trailer

        if not all([equipment_id, equipment_type]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # 테이블 매핑
        table_mapping = {
            "truck": "Truck",
            "chassis": "Chassis",
            "container": "Container",
            "trailer": "Trailer",
        }

        if equipment_type not in table_mapping:
            return jsonify({"success": False, "message": f"Invalid equipment type: {equipment_type}"}), 400


        # Zone Status 변경경
        query = f"""
            UPDATE Zone
            SET Status='Available'
            WHERE Zone_ID In (
                SELECT Zone_ID FROM {table_mapping[equipment_type]}
                WHERE {table_mapping[equipment_type]}_ID = :equipment_id
            )
        """
        db.session.execute(
            text(query),
            {"equipment_id": equipment_id},
        )
        db.session.commit()

        # 데이터베이스에서 해당 장비 삭제
        query = f"""
        INSERT INTO {table_mapping[equipment_type]}_Archive SELECT * FROM {table_mapping[equipment_type]} WHERE {table_mapping[equipment_type]}_ID=:equipment_id;
        DELETE FROM {table_mapping[equipment_type]} WHERE {table_mapping[equipment_type]}_ID=:equipment_id;
        """

        # DELETE FROM {table_mapping[equipment_type]}
        # WHERE {table_mapping[equipment_type]}_ID = :equipment_id

        db.session.execute(
            text(query),
            {"equipment_id": equipment_id},
        )
        db.session.commit()
        

        db.session.commit()
        return jsonify({"success": True, "message": f"{equipment_type.capitalize()} deleted successfully!"}), 200

    except Exception as e:
        db.session.rollback()  # 롤백 처리
        return jsonify({"success": False, "message": "Error deleting equipment", "error": str(e)}), 500



# Flask 애플리케이션 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)