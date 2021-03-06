from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from account.models import Profile, Main_Message
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def get_client_ip(request): #접속자 ip구하기
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required(login_url='/account/login/')
def detail(request, blog_id):
    Main_Message_Show = Main_Message.objects.get(id=1)
    location = request.session.get('location','first')
    selected_id = request.session.get('selected_id','none')
    profile=Profile.objects.get(
        user=request.user
    )
    if profile.UserType == "0": #권한 대기중 만들기 위해서
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

        

        content = {
            "posts_u":posts_u,
            "posts":posts,
            "posts_p":posts_p,
            "errorauth":"[메시지]\n회원가입 후\n관리자에게 권한을 부여 받아야\n글을 쓰거나 확인 할 수 있습니다!\n(관리자에게 카톡하세요!)",
            "errorauth_set":"block",
            "big_message":Main_Message_Show.big_message,
            "middle_message":Main_Message_Show.middle_message,
            "low_message":Main_Message_Show.low_message,
            "d_day_message":Main_Message_Show.d_day_message,
            "d_day_year":Main_Message_Show.d_day_year,
            "d_day_month":Main_Message_Show.d_day_month,
            "d_day_day":Main_Message_Show.d_day_day,
        }

        return render(request, "main.html", content)
    else: #권한 대기중 만들기 위해서
        if request.method == "POST" and "post_comment" in request.POST: #댓글 생성
            comment = Comment()
            comment.Article = Board.objects.get(pk=blog_id)
            comment.Body = request.POST.get('get_Body')
            comment.Author = request.user
            comment.Created_at = timezone.datetime.now()
            comment.save()
            return redirect('/board/detail/'+str(blog_id))
        elif request.method == "POST" and "delete_comment" in request.POST: #댓글 삭제
            comment = Comment.objects.get(pk=blog_id)
            comment.delete()
            return redirect('/board/detail/'+str(request.session.get('blog_id','')))
        else:
            blog_detail = get_object_or_404(Board, pk=blog_id)

            ########## 가까운 글 가져오기 #########
            if location == "myboard":
                near_detail_before = Board.objects.filter(Author=request.user, Created_at__lt=blog_detail.Created_at).order_by('-Created_at')#전에 만들어진 게시글 2개!! (마이페이지 일 경우)
                near_detail_after = Board.objects.filter(Author=request.user, Created_at__gt=blog_detail.Created_at).order_by('Created_at')#후에 만들어진 게시글 2개!! (마이페이지 일 경우)
            else:
                near_detail_before = Board.objects.filter(Category=blog_detail.Category, Created_at__lt=blog_detail.Created_at).order_by('-Created_at')#전에 만들어진 게시글 2개!!
                near_detail_after = Board.objects.filter(Category=blog_detail.Category, Created_at__gt=blog_detail.Created_at).order_by('Created_at')#후에 만들어진 게시글 2개!!

            check = 0 #2개까지만 최신 글들 불러오기 위해서 이렇게 했습니당!!
            near_detail = []
            near_detail2 = []
            for a in near_detail_before:
                near_detail.append(a)
                check+=1
                if check == 2:
                    check = 0
                    break

            for a in near_detail_after:
                near_detail2.append(a)
                check+=1
                if check == 2:
                    check = 0
                    near_detail2.reverse() #이 친구는 반전이 필요함!!
                    break

            ############ 가까운 글 가져오기 끝 ###########

            comments = Comment.objects.filter(Article__id=blog_id).order_by('Created_at')
            request.session['blog_id'] = blog_id #id 값을 가지고 온 이유는 modify 이용하기 위해서
            filename = blog_detail.files.name[6:] #파일 이름만 보이게 하려고
            filename2 = blog_detail.new_files.all() #파일 이름만 보이게 하려고
            user=request.user
            all_hit = Hitcount.objects.filter(IP=get_client_ip(request), Article__id=blog_id, date__gte=timezone.datetime.now()-datetime.timedelta(minutes=15))
            if all_hit: #여기서부터는 조회수를 만들기위해서 이 위에 all_hit부터 조회수
                pass
            else:
                try: #hittimecount라는 하나를 만들어서 조회수를 보여주기 하기 원래는 board자체에서 하려고 했는데 조회수가 늘어나면 수정되는 것 처럼 나와서... 결국 하나의 테이블을 더 만듬
                    hitviewcount = Hittimecount.objects.get(Article__id=blog_id)
                    hitviewcount.HowMuch = hitviewcount.HowMuch + 1 # title 수정
                    hitviewcount.save()
                except:
                    hitviewcount = Hittimecount()
                    hitviewcount.HowMuch = 1
                    hitviewcount.Article = Board.objects.get(pk=blog_id)
                    hitviewcount.save()

            hitcount = Hitcount()
            hitcount.Article = Board.objects.get(pk=blog_id)
            hitcount.IP = get_client_ip(request)
            hitcount.date = timezone.datetime.now()
            hitcount.save()
            content = {
                'blog':blog_detail,
                'Author':str(user),
                'filename':filename,
                'filename2':filename2,
                'comments':comments,
                'location':location,
                'near_detail_before':near_detail,
                'near_detail_after':near_detail2,
                "big_message":Main_Message_Show.big_message,
                "selected_id":selected_id
            }
            return render(request, 'detail.html', content)

@login_required(login_url='/account/login/')
def modify(request):
    Main_Message_Show = Main_Message.objects.get(id=1)
    blog_detail = get_object_or_404(Board, pk=request.session.get('blog_id',''))
    user=request.user
    profile=Profile.objects.get(
        user=request.user
    )
    if request.method == "POST": #전송했을 경우!
        blog_detail.Title = request.POST.get('get_title','')
        blog_detail.Body = request.POST.get('get_body','')
        blog_detail.files = False #파일 없을경우는 False로 올리고 있을 경우는 file녀석을 가져옴 (다중으로 가져오는 것을 추가해서 이제 필요가 없음! 하지만 전에 했던 것 때문에 유지중)
        blog_detail.images = request.FILES.get('pic', False)
        blog_detail.save()

        file_list = request.FILES.getlist('file')

        for item in file_list: 
            files = Files.objects.create(post=blog_detail, files=item)
            files.save()

        return redirect('/board/detail/'+str(blog_detail.id))
    return render(request, 'modify.html',{'blog':blog_detail, "big_message":Main_Message_Show.big_message,})

@login_required(login_url='/account/login/')
def delete(request):
    location = request.session.get('location','first') #메인페이지에서 수정했을 경우에는 first여서 바로 바탕화면으로
    selected_id = request.session.get('selected_id','none')
    if request.method == "POST":
        blog_detail = Board.objects.get(pk=request.session.get('blog_id',''))
        blog_detail.delete()
        if location == "first": #메인페이지에서 수정했을 경우에는 first여서 바로 바탕화면으로
            return redirect('/')
        elif location == "select_board":
            return redirect('/board/select_board/'+selected_id)
        elif location == "myboard":
            return redirect('/account/myboard/')
        else:
            return redirect('../'+str(location))
    else:
        return redirect('/')

def gallery(request):
    request.session['login_after'] = '/board/gallery/'
    gallery_b = Board.objects.filter(Category="2").order_by('-Created_at')
    if request.method == "POST":
        find_select = request.POST.get('find_select')
        gallery_b = Board.objects.filter(Category="2", Title__contains=find_select).order_by('-Created_at')
        pass
    paginator = Paginator(gallery_b,16) #페이지네이션 만들기
    page = request.GET.get('page') #페이지네이션 만들기
    posts = paginator.get_page(page) #페이지네이션 만들기
    request.session['location'] = 'gallery' #내 위치 알기 위해서 삭제한후 다시 돌아가기 위해서

    Main_Message_Show = Main_Message.objects.get(id=1)

    return render(request, "gallery.html", {'posts':posts, "big_message":Main_Message_Show.big_message})


def select_board(request, _id): #다른사람 작성한 글 보기
    Main_Message_Show = Main_Message.objects.get(id=1)

    try: # 해당 글쓴이가 없을 경우 예외처리
        profile = Profile.objects.get(user__id=_id)
        _user = profile.user
        _user_name = profile.Name
    except:
        _user = "None"
        _user_name = "None"

    my_b = Board.objects.filter(Author=_user).order_by('-Created_at')

    if request.method == "POST":
        find_select = request.POST.get('find_select')
        my_b = Board.objects.filter(Author=_user, Title__contains=find_select).order_by('-Created_at')
        pass

    paginator = Paginator(my_b,16) #페이지네이션 만들기
    page = request.GET.get('page') #페이지네이션 만들기
    posts = paginator.get_page(page) #페이지네이션 만들기
    request.session['location'] = 'select_board' #내 위치 알기 위해서 삭제한후 다시 돌아가기 위해서
    request.session['selected_id'] = _id

    return render(request, "select_board.html", {'user_id':_id, 'user_name':_user_name, 'posts':posts, 'my_b':my_b, "big_message":Main_Message_Show.big_message})

def _board(request, boardname):
    request.session['login_after'] = '/board/' + boardname + '/'
    Main_Message_Show = Main_Message.objects.get(id=1)
    if boardname == "notice":
        category = "0"
        request.session['location'] = 'notice' #내 위치 알기 위해서 삭제한후 다시 돌아가기 위해서
        board_name = "공지사항"
    elif boardname == "free":
        category = "1"
        request.session['location'] = 'free'
        board_name = "자유게시판"
    elif boardname == "study":
        category = "9"
        request.session['location'] = 'study'
        board_name = "공부게시판"
    board_find = boardname #게시글 찾기를 위해서 boardname에서 가져온 글을 저장한다!
    board_b = Board.objects.filter(Category=category).order_by('-Created_at')
    if request.method == "POST":
        find_select = request.POST.get('find_select')
        board_b = Board.objects.filter(Category=category, Title__contains=find_select).order_by('-Created_at')
        pass
    paginator = Paginator(board_b,16) #페이지네이션 만들기
    page = request.GET.get('page') #페이지네이션 만들기
    posts = paginator.get_page(page) #페이지네이션 만들기
    return render(request, "board.html", {'posts':posts, 'board_b':board_b, 'board_name':board_name, 'board_find':board_find, 'category':category, "big_message":Main_Message_Show.big_message})

@login_required(login_url='/account/login/')
def write(request):
    Main_Message_Show = Main_Message.objects.get(id=1)
    profile=Profile.objects.get(
        user=request.user
    )
    if profile.UserType == "0": #권한 대기중 만들기 위해서
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

        return render(request, "main.html", {"posts_u":posts_u, "posts":posts, "posts_p":posts_p, "errorauth":"[메시지]\n회원가입 후\n관리자에게 권한을 부여 받아야\n글을 쓰거나 확인 할 수 있습니다!\n(관리자에게 카톡하세요!)", "errorauth_set":"block", "big_message":Main_Message_Show.big_message})

    if request.method=="POST" and 'get_category' in request.POST: #만약 0 일경우는 공지사항 
        request.session['category'] = request.POST.get("category")
        if request.session.get('category','')=='0': #여기서 오류 뜨게 만들기!
            if profile.UserType=="99": #권한이 99일 경우 관리자다!
                board_name = "공지사항"
            else:
                del request.session['category'] #악용사항 없게
                board_b = Board.objects.filter(Category="0").order_by('-Created_at')
                paginator = Paginator(board_b,16) #페이지네이션 만들기
                page = request.GET.get('page') #페이지네이션 만들기
                posts = paginator.get_page(page) #페이지네이션 만들기
                return render(request,'board.html', {"error":"( 권한이 없습니다 )", "board_b":board_b, "posts":posts, "board_find":"0", "board_name":"공지사항", "big_message":Main_Message_Show.big_message})

        elif request.session.get('category','')=='1': #게시판 이름 보여주기
            board_name = "자유게시판"
        elif request.session.get('category','')=='2': #게시판 이름 보여주기
            board_name = "갤러리게시판"
        elif request.session.get('category','')=='3': #게시판 이름 보여주기
            board_name = "정보게시판"
        elif request.session.get('category','')=='4': #게시판 이름 보여주기
            board_name = "족보게시판"
        elif request.session.get('category','')=='9': #게시판 이름 보여주기
            board_name = "공부게시판"
        else:
            board_name = "오류"
        return render(request, "write.html", {'board_name':board_name, "big_message":Main_Message_Show.big_message})
    
    if request.session.get('category','')=='0' and request.method=="POST" and 'post' in request.POST: #여기는 저장하기
        if profile.UserType=="99": #권한이 99일 경우 관리자다!
            board_id = write_board(request) #글을 쓰고 return 값으로 id를 준다!
            return redirect('/board/detail/'+str(board_id))
        else:
            print("어디서 장난질?")

    elif request.method=="POST" and 'post' in request.POST:#아직 넣지는 않았지만 운영진일 경우 and 추가해서 넣기 물론 운영진 아니면 보이지도 않게 만들긴 templatetag로 할 것임
        board_id = write_board(request) #글을 쓰고 return 값으로 id를 준다!
        return redirect('/board/detail/'+str(board_id))
    else:
        pass

    return render(request, "write.html", {"big_message":Main_Message_Show.big_message})

def write_board(request): #글을 쓰는 값이다
    make = Board()
    make.Title = request.POST.get('get_title','')
    make.Body = request.POST.get('get_body','')
    make.Author = request.user
    make.Created_at = timezone.datetime.now()
    make.Category = request.session.get('category','')
    make.HowMuch = 0
    make.files = False #파일 없을경우는 False로 올리고 있을 경우는 file녀석을 가져옴
    make.images = request.FILES.get('pic', False)
    make.save()

    file_list = request.FILES.getlist('file')

    for item in file_list: 
        files = Files.objects.create(post=make, files=item)
        files.save()

    return make.id

