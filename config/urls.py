from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('apps.core.urls')),
    path('', include('apps.account.urls')),
    path('', include('apps.chat.urls')),
    path('admin/', admin.site.urls),
]
