from django.contrib import admin
from django.urls import path, include
from app.views import CardapioViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('cardapio', CardapioViewSet, basename='Cardapio')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
