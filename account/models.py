from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #1대1 조인
    Name = models.TextField(max_length=10) #이름
    UserNumber = models.IntegerField() #학번
    Phone = models.CharField(max_length=13) #전화번호
    UserType = models.CharField(max_length=13) #권한
    Generation = models.CharField(max_length=13) #기수

    def __str__(self):
        return '%s - %s' % (self.Name, self.Generation)

class Main_Message(models.Model): #메인페이지에 있는 영어들 관리자가 직접 수정할 수 있도록 만들기 위해서 만든 것!
    big_message = models.TextField(max_length=30)
    middle_message = models.TextField(max_length=30)
    low_message = models.TextField(max_length=30)
    d_day_message = models.TextField(max_length=30)
    d_day_year = models.CharField(max_length=30)
    d_day_month = models.CharField(max_length=30)
    d_day_day = models.CharField(max_length=30)

    def __str__(self):
        return '%s - %s' % (self.id, self.big_message)