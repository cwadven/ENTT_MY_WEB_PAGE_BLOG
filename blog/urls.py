from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('cwadven/', admin.site.urls),
    path('account/', include('account.urls')),
    path('board/', include('board.urls')),
    path('', include('main.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), #거짓으로 debug 만들고 보이게 하기
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), #거짓으로 debug 만들고 보이게 하기
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

