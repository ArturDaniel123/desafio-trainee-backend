from django.contrib import admin
from django.urls import path, include
from app.views import CardapioViewSet, RegistroViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('cardapio', CardapioViewSet, basename='Cardapio')
router.register('registro', RegistroViewSet, basename='Registro')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
