# fisa_streamlit_project
<hr>

## 🚽화장실 급하시죠?🚽

<br>

### 💩프로젝트 개요💩
- 목표: 사용자의 위치에서 가장 가까운 지하철역을 기준으로 무료로 이용할 수 있는 공중화장실 위치를 안내하는 서비스 제공
- 대상 사용자: 볼일이 급하지만 무료로 공중화장실을 찾고자 하는 사람들
<br>
<hr>

### 기능

1. 현재 위치 기반 역사공중화장실 및 주변 공중화장실 위치 조회 및 안내
2. 구 별로 공중화장실 위치 모아보기
<br>
<hr>

### 기술 스택

1. Frontend
    - <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=red">

2. Data-Processing
    - <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=Pandas&logoColor=orange">
    - <img src="https://img.shields.io/badge/Numpy-013243?style=for-the-badge&logo=Numepy&logoColor=blue">

3. Map
    - <img src="https://img.shields.io/badge/Folium-77B829?style=for-the-badge&logo=Folium&logoColor=green">
    - <img src="https://img.shields.io/badge/Javascript-F7DF1E?style=for-the-badge&logo=Javascript&logoColor=yellow">


<br>
<hr>

### 활용 데이터

|           데이터            |파일 형식|        출처        |
|----------------------------|---------|-------------------|
|서울교통공사_역사공중화장실정보|   csv   |    서울교통공사    |
| 서울시 공중화장실 위치정보    |   csv  |서울 열린데이터 광장 |
- 데이터 링크
    - [서울교통공사_역사공중화장실정보](https://www.data.go.kr/data/15044453/fileData.do)
    - [서울시 공중화장실 위치정보](https://data.seoul.go.kr/dataList/OA-162/S/1/datasetView.do?tab=A)

<br>

### 데이터 정제 내역

1. 미사용 컬럼 제거
    - 공중화장실 위치정보 데이터사용
        - 사용 컬럼: `구명`, `법정동명`, `위도`, `경도`
    - 역사공중화장실정보 데이터
        - 사용 컬럼: `운영노선명`, `역명`, `게이트 내외 구분`, `리모델링 연도`, `위도`, `경도`

2. 필요 컬럼 추가
    - 공중화장실 위치정보 데이터에 가까운 역 컬럼 추가
        - **Haversine 공식**을 활용해 각 공중화장실로부터 가장 가까운 지하철역 이름을 기입

3. 노이즈 데이터 처리
    - 공중화장실 위치정보 데이터
        - 잘못 기입된 구명 수정:
            - 예: `송파ㅜ` → `송파구`, `갈암구` → `강남구`, `구로수` → `구로구` → **서비스에 반영할 ‘서울 공중화장실’ 데이터 생성**

    - 역사공중화장실정보 데이터
        - `게이트 내외 구분` 값이 `내부`인 경우(사용료 발생) 제거
        - 리모델링 연도 `2008이전` 내역을 `2006`으로 일괄 수정
        - 하나의 지하철 역에 화장실 개수가 많은 케이스 중, 리모델링 년수까지 동일한 행 제거
        **→ 서비스에 반영할 ‘역사공중화장실정보’ 데이터 생성**

4. 구-역사 매핑 딕셔너리 생성
    - `{ '구명' : '역사명' }` 형태의 딕셔너리를 생성하여, 사용자가 구를 선택하면 해당 구에 속한 지하철역만 출력하도록 설계

<br>
<hr>

### streamlit 
1. 

<br>
<hr>

### 기대효과
- 사용자가 신속하고 정확하게 무료 공중화장실을 찾을 수 있도록 도움
- 서울 내 공중화장실 정보를 체계적으로 관리하고 사용자 친화적인 서비스를 제공
<br>
<hr>

### 🔥트러블슈팅
1. twwwwwww
2. 