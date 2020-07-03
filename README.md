### 쿠팡파트너스 크롤러

Scrapy + pyQt5 를 이용하여 크롤링구현

init.py로 시작하며 상품내용을 가진 현재시간.txt 및 상품사진(개별사진, 전체사진)을 가진 상품ID폴더가 생성

##### TODO

1. requirements.txt
2. app.py의 settings.set('DOWNLOAD_DELAY', 1.3)을 조절하여 크롤링 속도 조절

#### NOTE

분당 50회의 요청을 넘어가면 24시간 제한되며 3회 위반시 계정정지
프록시 작업을 하면 위의 제한을 피할 수 있다.

constants.py의 COUPANG_SEARCH_CATEGORIES 값이 사이트 업데이트에 따라 변경될 수 있음
