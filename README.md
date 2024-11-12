# 2024 Database PBL - Yard Management System (YMS)

## 팀 구성

| 팀원       | 직책   | 역할       |
| ---------- | ------ | ---------- |
| 오상영     | 팀장   | 백엔드     |
| 이재욱     | 개발자 | 백엔드     |
| 한륜헌     | 개발자 | 프런트엔드 |
| 바야스갈랑 | 개발자 | 프런트엔드 |
| 서영건     | 개발자 | 프런트엔드 |


---

## Yard Management System (YMS)

### 개요
저희의 YMS는 장비 관리에 특화된 시스템으로, Yard 내 장비와 사용자 관리를 효율적으로 수행하여 물류 흐름을 최적화하고 운영 효율성을 극대화하는 것을 목표로 합니다.



### 장비 관리의 중요성

장비는 회사의 중요한 자산으로, 관리가 제대로 이루어지지 않을 경우 다양한 손실로 이어질 수 있습니다. YMS는 장비 관리와 더불어 배송 물품의 효율적 관리에 중점을 두어 다음과 같은 이유로 운영의 필수적인 요소를 제공합니다:

1. **자산 관리**: 장비가 고장나거나 분실되거나 비효율적으로 운영될 경우 회사에 큰 비용적 손실을 초래할 수 있습니다. 따라서 장비의 상태를 지속적으로 관리하여 자원을 낭비하지 않고 최적화하는 것이 중요합니다.

2. **안전 관리**: 장비의 상태가 불량하면 안전사고 발생 가능성이 높아집니다. 이는 작업자와 장비 모두에 피해를 주고, 회사에 추가적인 금전적 손해를 유발할 수 있습니다. 장비 상태를 지속적으로 추적하여 이러한 위험을 방지할 필요가 있습니다.

3. **시간 관리**: 여러 화물을 동시다발적으로 처리해야 하는 Yard 환경에서는 시간 관리가 핵심입니다. 장비를 효율적으로 활용함으로써 작업 시간을 최적화하고 물류 처리 속도를 높이는 것이 필수적입니다.

4. **배송 물품 관리 및 추적**: 3PL(Third-Party Logistics) 서비스의 경우 물류 업체는 배송 중 물품 손상 시 배상 책임이 일반적입니다. YMS는 물품 관리 및 추적을 통해 물류 업체가 물품 손상에 대해 적절히 책임지거나 면책될 수 있도록 합니다.

---

### 주요 기능 및 설명

<details>
    <summary>장비 관리</summary>
    <h4>장비 관리</h4>
    <ol>
        <li><b>Yard 내 장비 이동</b>
            <ul>
                <li><b>설명</b>: Yard 내부에서 장비를 자유롭게 이동 가능하며, 드래그&드롭을 통해 직관적으로 조작할 수 있습니다.</li>
                <li><b>이유</b>: Yard 내 장비 위치는 물류 효율성에 중요한 영향을 미치며, 신속한 장비 이동을 통해 공간을 최적화하고 물류 흐름을 개선할 수 있습니다.</li>
            </ul>
        </li>
        <li><b>장비 연결 및 스케줄 할당</b>
            <ul>
                <li><b>설명</b>: 장비 연결(Truck, Truck + Chassis, Truck + Chassis + Container, Truck + Trailer)과 스케줄 할당(준비된 장비, 드라이버, 도착 장소, 출발 시간, 예정 도착 시간)을 지원합니다.</li>
                <li><b>이유</b>: 다양한 장비 조합에 유연하게 대응하며, 자원 배분 최적화와 불필요한 대기 시간 감소에 기여합니다.</li>
            </ul>
        </li>
        <li><b>로그 추적</b>
            <ul>
                <li><b>설명</b>: 장비 이동 내역을 기록하여 추적할 수 있습니다.</li>
                <li><b>이유</b>: 운영 투명성을 높이고 문제 발생 시 신속한 원인 파악과 안전성 강화를 위해 필수적입니다.</li>
            </ul>
        </li>
        <li><b>장비 증감 관리</b>
            <ul>
                <li><b>설명</b>: 장비를 추가하고 위치를 할당하는 기능을 지원합니다.</li>
                <li><b>이유</b>: 수요 변화와 사업 확장에 유연하게 대처하여 운영 효율성을 높입니다.</li>
            </ul>
        </li>
        <li><b>장비 유지 보수 및 수리 기록 관리</b>
            <ul>
                <li><b>설명</b>: 장비의 유지 보수와 수리 내역을 기록하고, 정기 점검 알림을 자동 제공하는 기능입니다.</li>
                <li><b>이유</b>: 장비 가동률을 극대화하고 장비 상태를 지속적으로 모니터링할 수 있습니다.</li>
            </ul>
        </li>
        <li><b>장비 활용도 분석</b>
            <ul>
                <li><b>설명</b>: 장비별 사용 빈도, 가동 시간, 비가동 시간을 분석하여 활용도를 평가합니다.</li>
                <li><b>이유</b>: 자원 효율적 배분을 위한 기초 자료로 활용됩니다.</li>
            </ul>
        </li>
        <li><b>장비 예약 시스템</b>
            <ul>
                <li><b>설명</b>: 장비 사용 일정을 사전 예약하여 필요한 시점에 장비를 확보할 수 있습니다.</li>
                <li><b>이유</b>: 작업 일정을 체계적으로 계획하여 장비 부족 상황을 방지하고 연속성 유지에 기여합니다.</li>
            </ul>
        </li>
        <li><b>장비 사고 및 문제 발생 기록</b>
            <ul>
                <li><b>설명</b>: 장비 관련 사고나 문제 발생 시 이를 기록하고 분석하여 위험 요소를 파악합니다.</li>
                <li><b>이유</b>: 운용의 안전성 강화와 리스크 관리를 위해 필수적입니다.</li>
            </ul>
        </li>
    </ol>
</details>
<details>
    <summary>사용자 관리</summary>
    <h4>사용자 관리</h4>
    <ol>
        <li><b>매니저 로그인 기능</b>
            <ul>
                <li><b>설명</b>: 매니저는 전체 장비와 자원의 흐름을 관리하며, 각 거점의 자원 배치와 스케줄을 조율할 수 있습니다.</li>
                <li><b>이유</b>: 매니저가 자원 배분과 흐름을 총괄함으로써 YMS 전체의 효율성을 높입니다.</li>
            </ul>
        </li>
        <li><b>드라이버 로그인 기능</b>
            <ul>
                <li><b>설명</b>: 드라이버가 자신의 스케줄을 확인하고 도착/출발 정보를 등록할 수 있습니다.</li>
                <li><b>이유</b>: 드라이버의 원활한 업무 수행과 정보 전달 정확성 증대를 위해 필수적입니다.</li>
            </ul>
        </li>
        <li><b>계정 추가 기능</b>
            <ul>
                <li><b>설명</b>: 개인 드라이버도 YMS 계정 생성할 수 있습니다.</li>
                <li><b>이유</b>: 회사 소속이 아닌 드라이버도 시스템에 등록할 수 있어야 하기 때문입니다.</li>
            </ul>
        </li>
    </ol>
</details>



---

## 팀 규칙

- 매주 화요일에 정기 회의
- 개발 완료 후, 각자 작업물을 `develop` 브랜치에 합치기

---

## 로컬 환경 구축 방법

### 1. docker 다운로드

공식 다운로드 링크: <a href="https://www.docker.com/products/docker-desktop/">도커 다운 링크</a>

### 2. git clone

```bash
git clone
cd .\2024_database_pbl\
```

### 3. docker-compose 실행

```bash
docker-compose up -b --build

### 4. flask 메인 페이지 접속 및 테스트

- 메인 페이지 : http://localhost:5000/
- db 연결 테스트 페이지 : http://localhost:5000/test_db
- db users 테이블 참조 페이지 : http://localhost:5000/users



### 번외

#### dbp_mysql_server 접속

```bash
docker exec -it mysql_server mysql -u root -p		# root 계정 접속
docker exec -it mysql_server mysql -u user -p		# user 계정 접속
```

root password : roow_password

user password : user_password



#### docker 이미지 컨트롤

1. 이미지 목록 확인

   ```bash
   docker images
   ```

2. 이미지 제거

   ```bash
   docker rmi [images_name or images_id]
   ```

   

#### docker container 컨트롤

1. container list 확인

   ```bash
   docker ps -a
   ```

2. container 시작

   ```bash
   docker start [container_name or container_id]
   ```

3. container 정지

   ```bash
   docker stop [container_name or container_id]
   ```

4. container 제거

   ```bash
   docker rm [container_name or container_id]
   ```