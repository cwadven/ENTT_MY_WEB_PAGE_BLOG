<h1 align="center">🌟Django 최초 나만의 홈페이지 구축🌟</h1>

나만의 홈페이지를 구축 후, Raspberry Pi 3에 연동시켜 배포까지 진행하기 위한 프로젝트

<h3 align="center">웹페이지</h3>
<p align="center">
<img alt="wkudorm" src="https://github.com/cwadven/ENTT_MY_WEB_PAGE_BLOG/blob/master/assets/seq1.PNG"/>
</p>

## 홈페이지 정보

<h3 align="center">공지사항</h3>
<p align="center">
<img alt="wkudorm" src="https://github.com/cwadven/ENTT_MY_WEB_PAGE_BLOG/blob/master/assets/seq2.PNG"/>
</p>

<h3 align="center">자유게시판</h3>
<p align="center">
<img alt="wkudorm" src="https://github.com/cwadven/ENTT_MY_WEB_PAGE_BLOG/blob/master/assets/seq3.PNG"/>
</p>

<h3 align="center">자유게시판 글</h3>
<p align="center">
<img alt="wkudorm" src="https://github.com/cwadven/ENTT_MY_WEB_PAGE_BLOG/blob/master/assets/seq4.PNG"/>
</p>

<h3 align="center">갤러리게시판</h3>
<p align="center">
<img alt="wkudorm" src="https://github.com/cwadven/ENTT_MY_WEB_PAGE_BLOG/blob/master/assets/seq6.PNG"/>
</p>

<h3 align="center">마이페이지</h3>
<p align="center">
<img alt="wkudorm" src="https://github.com/cwadven/ENTT_MY_WEB_PAGE_BLOG/blob/master/assets/seq5.PNG"/>
</p>

## 서비스 주소
**주소 :**<br>
https://dalgona.shop/<br>
현재는 닫혀져 있는 주소입니다!
<br><br>

## 개발자

**👤 이창우**

- Github : https://github.com/cwadven
- Backend : Django
- Service : Nginx, SQLite, SSL
- Server : Nginx, uwsgi
- 기술스택 : Django
- 개발기간 : <br>
    - 2019년 12월 21일 ~ 2020년 1월 18일
    - 2020년 1월 18일 ~ 필요에 따라 (버그 수정 및 Nginx 라즈베리파이로 배포)

## 환경 구축

~~~
1. python -m venv myvenv (가상환경 생성)
2. python source myvenv/Script/activates (가상환경 실행)
3. pip install -r requirements.txt (의존성 모듈 설치)
4. python manage.py collectstatic (static 파일 생성)
8. python manage.py migrate (세션 테이블 생성)
10. python manage.py runserver
~~~

## 참고

라즈베리파이 3에 배포를 하였는데 속도가 너무 느리다...
그래서 결국 안쓰게 되었다고 합니다 ㅎ!!

2020년 11월 도중 SD카드가 고장이나서 문제가 생겼습니다...
2020-12-31 다시 복구... 복구하면서 ssl 적용
