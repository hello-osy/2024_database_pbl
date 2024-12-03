### Docker new mysql container setup

```bash
docker-compose up -d

docker exec -it dbp_mysql_server mysql -u user -p	# mysql 서버 접속

localhost:5000		# flask 페이지
```



### Docker 실행중인 컨테이너 컨트롤

### 실행중인 컨테이너 확인

```bash
docker ps
docker ps -a #중지된 컨테이너 포함 전체 컨테이너 확인
```



#### Docker 실행중인 컨테이너 종료

```bash
docker stop [컨테이너 이름]
```



### Docker 이미지를 파일로 저장하고 전달하기

Docker 이미지를 파일로 내보내서 이메일이나 파일 공유 서비스를 통해 전달할 수도 있습니다.

#### 이미지 저장하기

1. **컨테이너 이미지 파일로 저장**:

   - 현재 컨테이너의 상태를 이미지로 저장하고 싶다면 `docker commit` 명령어를 사용

     ```bash
     docker commit mysql_server custom_mysql_image
     ```

2. **이미지 파일로 내보내기**:

   - `docker save` 명령어를 사용하여 Docker 이미지를 `.tar` 파일로 저장할 수 있습니다.

     ```bash
     docker save -o custom_mysql_image.tar custom_mysql_image
     ```

   - 이 명령어는 현재 로컬에 있는 `custom_mysql_image` 이미지를 `custom_mysql_image.ta` 파일로 내보냅니다.

3. **파일 전달**:

   - 생성된 `custom_mysql_image.tar` 파일을 이메일, 클라우드 드라이브, 또는 USB 드라이브를 통해 공유할 수 있습니다.

#### 이미지 파일 가져오기

상대방이 이미지를 가져올 때는 `docker load` 명령어를 사용합니다.

```bash
docker load -i custom_mysql_image.tar
```

이 명령어를 실행하면 해당 이미지가 로컬 Docker 이미지 목록에 추가됩니다.



<span style="color:red;font-weight:bold;">문제 발생</span>: 이미지 가져오는데 한평생 걸림 => docker hub 사용해야 할듯



## Docker Hub

### 1. Docker Hub에 이미지 업로드하기

#### 1-1. Docker Hub 계정 생성 및 로그인

먼저, Docker Hub에서 계정을 만듭니다. 이후 로컬 터미널에서 Docker Hub에 로그인합니다.

```bash
docker login
```

명령어를 실행하면 Docker Hub의 사용자 이름과 비밀번호를 입력하라는 메시지가 나타납니다.

#### 1-2. Docker 이미지에 태그 추가

이미지를 Docker Hub에 업로드하려면 **이미지에 Docker Hub 사용자 이름을 포함한 태그**를 추가해야 합니다. 예를 들어, Docker Hub 사용자 이름이 `username`이고, 이미지 이름이 `myapp`이라면 다음과 같이 태그를 추가합니다.

```bash
docker tag local_image_name username/myapp:latest
```

예시:

```bash
docker tag dbp_mysql_server_image username/dbp_mysql_server_image:latest
```

여기서:

- `local_image_name`은 로컬에 있는 이미지의 이름입니다.
- `username/myapp:latest`는 Docker Hub에 업로드될 이미지 이름과 태그입니다.

#### 1-3. Docker Hub에 이미지 푸시

이제 Docker Hub에 이미지를 푸시합니다.

```bash
docker push username/dbp_mysql_server_image:latest
```

이 명령어를 실행하면 Docker가 로컬 이미지를 Docker Hub의 `username/dbp_mysql_server_image:latest` 레포지토리로 업로드합니다.

#### 1-4. DB내 데이터 백업하기

```bash
docker run --rm --volumes-from dbp_mysql_server -v %cd%/backup:/backup ubuntu bash -c "cd /var/lib/mysql && tar cvf /backup/mysql_data.tar --exclude='ibdata1' --exclude='ib_logfile*' --exclude='mysql.ibd' --exclude='undo_001' --exclude='undo_002' --exclude='auto.cnf' --exclude='server-cert.pem' --exclude='server-key.pem' ."
```

mysql 서버 내에 있는 데이터를 **cmd**로 백업한다. 

기존 image에는 계정 정보와 DB 스키마 정보가 사라지기 때문에 해당 정보를 백업, 공유해야한다.



### 2. 다른 사용자가 이미지를 사용하는 방법

#### 2-1. Docker Hub에서 image pull

이미지를 Docker Hub에 업로드한 후, 다른 사용자들은 간단히 `docker pull` 명령어로 해당 이미지를 가져올 수 있습니다.

```bash
docker pull username/dbp_mysql_server_image:latest
```

이 명령어를 실행하면 Docker가 Docker Hub에서 이미지를 다운로드하여 로컬 환경에 저장합니다. 이제 다른 사용자는 이 이미지를 사용하여 컨테이너를 실행할 수 있습니다.

#### 2-2. 백업 데이터 적용

```bash
docker run --rm --volumes-from dbp_mysql_server -v $(pwd)/backup:/backup ubuntu bash -c "cd /var/lib/mysql && tar cvf /backup/mysql_data.tar ."

docker run --rm -v %cd%\backup:/backup -v mysql_data:/var/lib/mysql ubuntu bash -c "cd /var/lib/mysql && tar xvf /backup/mysql_data.tar --exclude='ibdata1' --exclude='ib_logfile*'"
```





#### 예시: 컨테이너 실행

이미지를 다운로드한 후, 다음 명령어로 컨테이너를 실행할 수 있습니다.

```bash
docker run -d --name my_container_name username/dbp_mysql_server_image:latest
```

- **`-d`**: 백그라운드에서 컨테이너 실행
- **`--name`**: 컨테이너 이름 설정
- **`username/dbp_mysql_server_image:latest`**: Docker Hub에서 받은 이미지 이름과 태그

### 3. `docker-compose`로 여러 사용자와 쉽게 공유하기

Docker Compose 파일을 사용하여 여러 사용자와 쉽게 공유할 수 있습니다. `docker-compose.yml` 파일에 Docker Hub에서 다운로드할 이미지 정보를 추가해두면, 다른 사용자는 `docker-compose up` 명령어만으로 설정된 모든 컨테이너를 실행할 수 있습니다.

예시 `docker-compose.yml` 파일:

```
version: '3.8'

services:
  mysql_server:
    image: username/dbp_mysql_server_image:latest
    container_name: mysql_server
    ports:
      - "3306:3306"
```

다른 사용자는 `docker-compose.yml` 파일을 받고 다음 명령어로 컨테이너를 실행할 수 있습니다.

```bash
docker-compose up -d
```

### 요약

1. **Docker Hub에 이미지 업로드**: `docker login` → `docker tag` → `docker push`.
2. **다른 사용자 사용 방법**: `docker pull`로 이미지를 받고 `docker run` 또는 `docker-compose up`으로 컨테이너를 실행.



<span style="color:red;font-weight:bold;">문제 발생</span>: 데이터 백업을 2시간정도 시도해 봤는데 안됌 -> docker-compose 단계에서 다이렉트로 추가하게 설정



