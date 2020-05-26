from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('gallery/', views.gallery, name='gallery'),
    path('write/', views.write, name='write'),
    path('modify/', views.modify, name='modify'),
    path('delete/', views.delete, name='delete'),
    path('detail/<int:blog_id>', views.detail, name='detail'),
    path('<boardname>/', views._board, name='_board'),
    path('select_board/<_id>/', views.select_board, name='select_board'),
]