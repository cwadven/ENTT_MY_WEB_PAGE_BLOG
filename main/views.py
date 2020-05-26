from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from board.models import *
from account.models import *
from django.core.paginator import Paginator
import json
import requests
from django.db.models import Q


def main(request): #바꿀 경우 detail 부분도 바꿔줘야 한다!!
    request.session['login_after'] = '/'
    try:
        response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Iksan&appid=c4d586561f37629e756e7c428f3d2eea', params=requests.get) #rest 같은녀석 함수
        geodata = response.json()
        main_response = geodata["main"]
        temp = int(float(main_response["temp"])-273.15)
    except:
        temp = "ERROR"

    recent = Board.objects.all().order_by('-Created_at')
    paginator = Paginator(recent,5) #페이지네이션 만들기
    page = request.GET.get('page') #페이지네이션 만들기
    posts = paginator.get_page(page) #페이지네이션 만들기

    recent_u = Board.objects.all().order_by('-Updated_at')
    paginator_u = Paginator(recent_u,5) #페이지네이션 만들기
    page_u = request.GET.get('page') #페이지네이션 만들기
    posts_u = paginator_u.get_page(page_u) #페이지네이션 만들기

    seen = []
    posts_p = []

    popular_p = Hittimecount.objects.all().order_by('-HowMuch')[:5] # 인기글 가져오는 것 만들기!
    for gets in popular_p:
        seen.append(gets.Article.id)

    for i in range(len(seen)):
        posts_p.append(Board.objects.get(id=seen[i]))

    Main_Message_Show = Main_Message.objects.get(id=1)

    content = {
            "errorauth_set":"none",
            "posts":posts,
            "posts_u":posts_u,
            "posts_p":posts_p,
            "temp":temp,
            "big_message":Main_Message_Show.big_message,
            "middle_message":Main_Message_Show.middle_message,
            "low_message":Main_Message_Show.low_message,
            "d_day_message":Main_Message_Show.d_day_message,
            "d_day_year":Main_Message_Show.d_day_year,
            "d_day_month":Main_Message_Show.d_day_month,
            "d_day_day":Main_Message_Show.d_day_day
        }

    return render(request, "main.html", content)

def ajax(request):
    if request.is_ajax():
        login_after = request.session.get('login_after','/')
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponse(json.dumps({'message':'1', 'login_after':login_after}), 'application/json')
        else:
            return HttpResponse(json.dumps({'message':'<br>아이디 혹은 비밀번호가 불일치 합니다.'}), 'application/json')


'''
def signin(request):
    recent = Board.objects.all().order_by('-Created_at')
    paginator = Paginator(recent,5) #페이지네이션 만들기
    page = request.GET.get('page') #페이지네이션 만들기
    posts = paginator.get_page(page) #페이지네이션 만들기

    recent_u = Board.objects.all().order_by('-Updated_at')
    paginator_u = Paginator(recent_u,5) #페이지네이션 만들기
    page_u = request.GET.get('page') #페이지네이션 만들기
    posts_u = paginator_u.get_page(page_u) #페이지네이션 만들기

    return render(request, "main.html", {"errorauth_set":"none", "posts":posts, "posts_u":posts_u, "temp":temp})
'''