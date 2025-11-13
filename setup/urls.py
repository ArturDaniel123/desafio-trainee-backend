from django.contrib import admin
from django.urls import path
from app.views import Pratos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pratos/', Pratos)
]
