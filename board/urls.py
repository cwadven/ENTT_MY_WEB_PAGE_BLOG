from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('notice/', views.notice_board, name='notice_board'),
    path('write/', views.write, name='write'),
    path('modify/', views.modify, name='modify'),
    path('free/', views.free, name='free'),
    path('study/', views.study, name='study'),
    path('gallery/', views.gallery, name='gallery'),
    path('delete/', views.delete, name='delete'),
    path('detail/<int:blog_id>', views.detail, name='detail'),
]