from django.db import models
from django.utils import timezone
import datetime
from account.models import Profile



class Board(models.Model):
    Title = models.CharField(max_length=50) #제목
    Body = models.TextField() #내용
    Created_at = models.DateTimeField(auto_now_add=True) #생성 일자 및 시간
    Updated_at = models.DateTimeField(auto_now=True) #수정 일자 및 시간
    Author = models.CharField(max_length=13) #글쓴이 아이디
    Category = models.CharField(max_length=13) #분류
    HowMuch = models.IntegerField() #조회수
    files=models.FileField(upload_to='files/', default='')
    images=models.FileField(upload_to='Sumnail/', default='')

    def __str__(self):
        return '%s - %s' % (self.Title, self.id)

    def get_generation(self): #이름을 나오게 하는데 예외처리 까지 적용 만약 탈퇴한 사람이면!! Id 가 나온다
        try:
            a = Profile.objects.get(user__username=self.Author)
            if a.UserType == "99":
                return "<span style='font-weight:bolder;color:orangered;'>"+a.Name+"("+a.Generation+"기)</span>"
            elif a.UserType == "98": #관리자 및 운영진
                return "<span style='font-weight:bolder;color:blue;'>"+a.Name+"("+a.Generation+"기)</span>"
            elif a.UserType == "3": #손님
                return "<span style='font-weight:bolder;color:darkviolet;'>"+a.Name+"("+a.Generation+"기)</span>"
            else: #일반 사용자
                return "<span style='font-weight:bolder;color:black;'>"+a.Name+"("+a.Generation+"기)</span>"
        except: #익명을 위해서 id나오게 삭제되니깐 이름은 알 수 없으므로...
            return "<span style='font-weight:bolder;color:grey;'>"+self.Author+"</span>"

    def get_Phone(self):
        try:
            a = Profile.objects.get(user__username=self.Author)
            return a.id#a.Phone
        except: 
            return "없습니다"


    def new(self): #최신
        if self.Created_at > timezone.now() - datetime.timedelta(days=1):
            return "<img height='16px' src='/static/n.png'/>"
        else:  #하루 지나면 안 최신
            return ""

    def change(self): #최신
        if self.Updated_at > timezone.now() - datetime.timedelta(days=1):
            return "<img height='16px' src='/static/c.png'/>"
        else:  #하루 지나면 안 최신
            return ""
    
    def file_icon(self): #최신
        if len(self.files.name) > 5: #5글자 이상일경우로 했음!! 그러면 당연히 5글자 이상 아닌게 없을 것임!
            return "<img height='16px' src='/static/file.png'/>"
        elif self.new_files.all():  #하루 지나면 안 최신
            return "<img height='16px' src='/static/file.png'/>"
        else:
            return ""

    def sumnail_detail(self): #최신
        if len(self.images.name) > 5: #5글자 이상일경우로 했음!! 그러면 당연히 5글자 이상 아닌게 없을 것임!
            return "<img style='width:100%' src="+self.images.url+"/>"
        else:  #하루 지나면 안 최신
            return ""

    def howmanycomment(self):
        a = Comment.objects.filter(Article=self.id).count()
        b = str('[') + str(a) + str(']')
        if a:
            return b
        else:
            return ""

    def howmanyhit(self):
        a = Hittimecount.objects.get(Article=self.id)
        if a:
            return str("<img height='16px' src='/static/eye.png'/> ") + str(a.HowMuch)

    def summary(self):
        if(len(self.Body)>50):
            return self.Body[:49] + "..."
        else:
            return self.Body

class Comment(models.Model):
    Article = models.ForeignKey(Board, on_delete=models.CASCADE)
    Author = models.CharField(max_length=13)
    Body = models.TextField() #내용
    Created_at = models.DateTimeField(auto_now_add=True) #생성 일자 및 시간
    Updated_at = models.DateTimeField(auto_now=True) #수정 일자 및 시간

    def __str__(self):
        return '%s - %s' % (self.Body, self.Name)

    def get_generation(self):
        try:
            a = Profile.objects.get(user__username=self.Author)
            if a.UserType == "99":
                return "<span style='font-weight:bolder;color:orangered;'>"+a.Name+"("+a.Generation+"기)</span>"
            elif a.UserType == "98": #관리자 및 운영진
                return "<span style='font-weight:bolder;color:blue;'>"+a.Name+"("+a.Generation+"기)</span>"
            elif a.UserType == "3": #손님
                return "<span style='font-weight:bolder;color:darkviolet;'>"+a.Name+"("+a.Generation+"기)</span>"
            else: #일반 사용자
                return "<span style='font-weight:bolder;color:black;'>"+a.Name+"("+a.Generation+"기)</span>"
        except: #익명을 위해서 id나오게 삭제되니깐 이름은 알 수 없으므로...
            return "<span style='font-weight:bolder;color:grey;'>"+self.Author+"</span>"

class Hitcount(models.Model):#모든 조회수
    Article = models.ForeignKey(Board, on_delete=models.CASCADE)
    IP = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.IP, self.Article)

class Hittimecount(models.Model):
    Article = models.ForeignKey(Board, on_delete=models.CASCADE)
    HowMuch = models.IntegerField() #조회수

    def __str__(self):
        return '%s - %s' % (self.Article, self.HowMuch)

class Files(models.Model):
    Created_at = models.DateTimeField(auto_now_add=True) #생성 일자 및 시간
    Updated_at = models.DateTimeField(auto_now=True) #수정 일자 및 시간
    post = models.ForeignKey(Board, related_name='new_files', on_delete=models.CASCADE)
    files = models.FileField(blank=True, null=True, upload_to='files/')

    def __str__(self):
        return '{} - {}'.format(self.post, self.files)