from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from insightapp import endpoints




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(endpoints)),
    path('api/auth/', include('knox.urls')),
]
