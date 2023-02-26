
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('referal_site.urls')),
    path("admin/", admin.site.urls),
]
