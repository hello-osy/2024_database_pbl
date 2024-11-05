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

## 웹 링크

- **개발용 링크**: [https://vercel.com/limulu-ks-projects/db/6G1NcvdXsQQLHDUD8KfCDA2vXCn9](https://vercel.com/limulu-ks-projects/db/6G1NcvdXsQQLHDUD8KfCDA2vXCn9)
- **사용자용 링크**: [https://db-ecru.vercel.app/](https://db-ecru.vercel.app/)

---

## Yard Management System (YMS)

### 개요
YMS는 Yard 내 장비와 사용자 관리를 효율적으로 수행하기 위한 시스템입니다. 이를 통해 물류 흐름 최적화와 운영 효율성을 극대화할 수 있습니다.

### 주요 기능 및 설명

#### 장비 관리

1. **Yard 내 장비 이동**
   - **설명**: Yard 내부에서 장비를 자유롭게 이동 가능하며, 드래그&드롭을 통해 직관적으로 조작할 수 있습니다.
   - **이유**: Yard 내 장비 위치는 물류 효율성에 중요한 영향을 미치며, 신속한 장비 이동을 통해 공간을 최적화하고 물류 흐름을 개선할 수 있습니다.

2. **장비 연결 및 스케줄 할당**
   - **설명**: 장비 연결(Truck, Truck + Chassis, Truck + Chassis + Container, Truck + Trailer)과 스케줄 할당(준비된 장비, 드라이버, 도착 장소, 출발 시간, 예정 도착 시간)을 지원합니다.
   - **이유**: 다양한 장비 조합에 유연하게 대응하며, 자원 배분 최적화와 불필요한 대기 시간 감소에 기여합니다.

3. **로그 추적**
   - **설명**: 장비 이동 내역을 기록하여 추적할 수 있습니다.
   - **이유**: 운영 투명성을 높이고 문제 발생 시 신속한 원인 파악과 안전성 강화를 위해 필수적입니다.

4. **장비 증감 관리**
   - **설명**: 장비를 추가하고 위치를 할당하는 기능을 지원합니다.
   - **이유**: 수요 변화와 사업 확장에 유연하게 대처하여 운영 효율성을 높입니다.

5. **장비 유지 보수 및 수리 기록 관리**
   - **설명**: 장비의 유지 보수와 수리 내역을 기록하고, 정기 점검 알림을 자동 제공하는 기능입니다.
   - **이유**: 장비 가동률을 극대화하고 장비 상태를 지속적으로 모니터링할 수 있습니다.

6. **장비 활용도 분석**
   - **설명**: 장비별 사용 빈도, 가동 시간, 비가동 시간을 분석하여 활용도를 평가합니다.
   - **이유**: 자원 효율적 배분을 위한 기초 자료로 활용됩니다.

7. **장비 예약 시스템**
   - **설명**: 장비 사용 일정을 사전 예약하여 필요한 시점에 장비를 확보할 수 있습니다.
   - **이유**: 작업 일정을 체계적으로 계획하여 장비 부족 상황을 방지하고 연속성 유지에 기여합니다.

8. **장비 사고 및 문제 발생 기록**
   - **설명**: 장비 관련 사고나 문제 발생 시 이를 기록하고 분석하여 위험 요소를 파악합니다.
   - **이유**: 운용의 안전성 강화와 리스크 관리를 위해 필수적입니다.

#### 사용자 관리

1. **매니저 로그인 기능**
   - **설명**: 매니저는 전체 장비와 자원의 흐름을 관리하며, 각 거점의 자원 배치와 스케줄을 조율할 수 있습니다.
   - **이유**: 매니저가 자원 배분과 흐름을 총괄함으로써 YMS 전체의 효율성을 높입니다.

2. **드라이버 로그인 기능**
   - **설명**: 드라이버가 자신의 스케줄을 확인하고 도착/출발 정보를 등록할 수 있습니다.
   - **이유**: 드라이버의 원활한 업무 수행과 정보 전달 정확성 증대를 위해 필수적입니다.

---

## 팀 규칙

- 매주 화요일에 정기 회의
- 개발 완료 후, 각자 작업물을 `develop` 브랜치에 합치기

---

## 로컬 환경 구축 방법

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
