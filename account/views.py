from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile, Main_Message
from board.models import Board
from django.http import HttpResponse
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

@login_required(login_url='/account/login/')
def myboard(request):
    my_b = Board.objects.filter(Author=request.user).order_by('-Created_at')
    if request.method == "POST":
        find_select = request.POST.get('find_select')
        my_b = Board.objects.filter(Author=request.user, Title__contains=find_select).order_by('-Created_at')
        pass
    paginator = Paginator(my_b,16) #페이지네이션 만들기
    page = request.GET.get('page') #페이지네이션 만들기
    posts = paginator.get_page(page) #페이지네이션 만들기
    request.session['location'] = 'myboard' #내 위치 알기 위해서 삭제한후 다시 돌아가기 위해서
    return render(request, "myboard.html", {'posts':posts, 'my_b':my_b})

def findpassword(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        if User.objects.filter(username=username).exists():
            user=User.objects.get(
            username=request.POST.get('username')
            )
            profile = Profile.objects.get(user__username=username)
            if profile.Phone == request.POST.get("phone"):
                new_password = request.POST.get("changepw1")
                password_confirm = request.POST.get("changepw2")
                if new_password == password_confirm: #새로운 비밀번호와 비밀번호 확인비교
                    user.set_password(new_password)
                    user.save()
                    auth.login(request,user)
                    return redirect('/')
                else:
                    return render(request, "findpassword.html", {"error":"새로운 비밀번호와 비밀번호 확인이 다릅니다!"})
            else:
                return render(request, "findpassword.html", {"error":"사용자의 정보가 틀렸습니다!"})
        else:
            return render(request, "findpassword.html", {"error":"해당사용자는 존재하지 않습니다!"})
    return render(request, "findpassword.html")

@login_required(login_url='/account/login/')
def userupdate(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user__username=request.user)
        profile.Phone = request.POST.get("phone")
        profile.save()
        return redirect('/account/mypage/')
    return render(request, "userupdate.html")

@login_required(login_url='/account/login/')
def deleteacc(request):
    if request.method == 'POST':
        user = User.objects
        if request.POST.get("confirm") == "탈퇴": #만약 탈퇴이면 필터링된 녀석들 전부 삭제를 한다!!
            request.user.delete() #유저 삭제하면 자동적으로 참조되서 Profile은 삭제됨          
            return redirect('/')
        else:
            return render(request, "delete.html", {"error":"오타입니다. '탈퇴'를 입력해주세요."})
    return render(request, "delete.html")

@login_required(login_url='/account/login/')
def mypage(request):
    profile = Profile.objects.get(user__username=request.user)
    content = {
        'profile':profile
    }
    return render(request, "mypage.html", content)

def signup(request):
    if request.method == "POST" and 'signup_submit' in request.POST:
        if request.POST["password1"]==request.POST["password2"]:
            now = datetime.datetime.now()
            user = User.objects.create_user(
                username=request.POST["username_id"],
                password=request.POST["password1"]
            )
            profile = Profile( #회원가입 저장
                user=user,
                Name=request.POST.get("name"),
                UserNumber=int(request.POST.get("id_num")),
                Phone=request.POST.get("phone"),
                UserType="0",
                Generation=str((int(now.year) - 1989)),
            )
            profile.save()
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, '비밀번호 확인이 잘못되었습니다')
            return render(request, "signup.html")
            
    return render(request, "signup.html")

def login(request):
    request.session['login_after'] = request.GET.get("next", "/")
    return render(request, "loginplease.html")

def logout(request):
    auth.logout(request)
    return redirect("/")

def check(request):
    username = request.POST.get("username_id")
    user_check = User.objects.filter(username=username)

    if user_check.exists():
        return HttpResponse(json.dumps({'message':'<font color=red>해당 아이디는 존재합니다!</font>', 'state':'0'}), 'application/json')
    else:
        return HttpResponse(json.dumps({'message':'<font color=blue>해당 아이디 사용가능!</font>', 'state':'1'}), 'application/json')
        
@login_required(login_url='/account/login/')
def main_message(request):
    profile = Profile.objects.get(user__username=request.user)
    if profile.UserType == "99" or profile.UserType == "98":
        Main_Message_Show = Main_Message.objects.get(id=1)
        if request.method == 'POST':
            Main_Message_Show.big_message = request.POST.get("big_message")
            Main_Message_Show.middle_message = request.POST.get("middle_message")
            Main_Message_Show.low_message = request.POST.get("low_message")
            Main_Message_Show.d_day_message = request.POST.get("d_day_message")
            Main_Message_Show.d_day_year = request.POST.get("d_day_year")
            Main_Message_Show.d_day_month = request.POST.get("d_day_month")
            Main_Message_Show.d_day_day = request.POST.get("d_day_day")
            Main_Message_Show.save()
        content={
            "big_message":Main_Message_Show.big_message,
            "middle_message":Main_Message_Show.middle_message,
            "low_message":Main_Message_Show.low_message,
            "d_day_message":Main_Message_Show.d_day_message,
            "d_day_year":Main_Message_Show.d_day_year,
            "d_day_month":Main_Message_Show.d_day_month,
            "d_day_day":Main_Message_Show.d_day_day
        }
        return render(request, "main_message.html", content)
    else:
        return redirect("/account/mypage/")
        
@login_required(login_url='/account/login/')
def permission(request):
    profile = Profile.objects.get(user__username=request.user)
    if profile.UserType == "99":
        profile_all = Profile.objects.all().order_by('-UserType','-Generation')
    else:
        profile_all = Profile.objects.filter(~(Q(UserType = 99) | Q(UserType = 98))).order_by('UserType').order_by('-Generation') #운영자는 관리자 끼리 못지운다
    if profile.UserType == "99" or profile.UserType == "98":
        if request.method == 'POST':
            Profile_change = Profile.objects.get(id=request.POST.get("id"))
            Profile_change.UserType = request.POST.get("permission_number")
            Profile_change.Generation = request.POST.get("Generation")
            Profile_change.save()
        content = {
            "users":profile_all
        }
        return render(request, "permission.html", content)
    else:
        return redirect("/account/mypage/")

@login_required(login_url='/account/login/')
def force_delete(request): #강제 탈퇴 시키기
    if request.method == 'POST':
        profile = Profile.objects.get(user__username=request.user)
        if profile.UserType == "99" or profile.UserType == "98": #예외처리를 위해서
            Profile_change = Profile.objects.get(id=request.POST.get("id"))
            if Profile_change.Name == request.POST.get("name"): #이름과 맞으면! 아닐경우는 아무것도 안한다! 이유는 사용자가 바꿔서 강제로 삭제할 수 있을 경우를 대비해서 작성
                user=User.objects.get( #user 테이블에서 직접 삭제하기
                username=Profile_change.user.username
                )
                user.delete()
                return redirect("/account/permission/")