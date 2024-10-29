# 2024_database_pbl

## 팀 구성

| 팀원       | 직책   | 역할       |
| ---------- | ------ | ---------- |
| 오상영     | 팀장   | 벡엔드     |
| 이재욱     | 개발자 | 벡엔드     |
| 한륜헌     | 개발자 | 프런트엔드 |
| 바야스갈랑 | 개발자 | 프런트엔드 |
| 서영건     | 개발자 | 프런트엔드 |



## 웹 링크

- 개발용 링크 : https://vercel.com/limulu-ks-projects/db/6G1NcvdXsQQLHDUD8KfCDA2vXCn9
- 사용자용 링크 : https://db-ecru.vercel.app/



## 목표

### Yard Management System 구현

- 장비 관리
  - yard 내 장비 이동
    - 드래그&드롭으로 내부에서의 장비 이동
  - yard 내 장비 연결 및 스케쥴 할당
    - 장비 연결 :
      1. Truck
      2. Truck + Chassis
      3. Truck + Chassis + Container 
      4. Truck + Trailer
    - 스케쥴 할당 : 준비된 장비, 드라이버, 도착 장소, 출발 시간, 예정 도착 시간
  - 로그 추적
  - 장비 증감
    - 장비 추가
    - 새 장비 위치 할당
- 사용자 관리
  - 로그인 -> 매니저
    - 장비 관리
    - 거점 관리
  - 로그임 -> 드라이버
    - 스케쥴 확인
    - 출발 및 도착 정보 등록



## 팀 규칙

- 매주 화요일에 모여서 회의
- 각자 개발 끝나면 develop 브랜치에 합치기



## 로컬에서 사용방법

### 1. node js 다운로드

```cmd
> npm -v
```



### 2. vercel 로컬 환경 구축

```cmd
> npm i -g vercel
> vercel login
> vercel .
```













