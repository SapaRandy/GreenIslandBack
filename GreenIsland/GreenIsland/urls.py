from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('plantid/', include('plantid.urls')),
    path('arduino/', include('plantid.urls_arduino'))
]
