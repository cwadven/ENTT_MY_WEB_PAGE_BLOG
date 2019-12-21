from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('mypage/', views.mypage, name='mypage'),
    path('myboard/', views.myboard, name='myboard'),
    path('delete/', views.deleteacc, name='delete'),
    path('findpassword/', views.findpassword, name='findpassword'),
    path('userupdate/', views.userupdate, name='userupdate'),
    path('usercheck/', views.check, name='usercheck'),
    path('main_message/', views.main_message, name='main_message'),
    path('permission/', views.permission, name='permission'),
    path('force_delete/', views.force_delete, name='force_delete'),
]