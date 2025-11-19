from django.contrib import admin
from django.urls import path, include
from app.views import CardapioViewSet, RegistroViewSet, PedidoViewSet, faturamento
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

router = routers.DefaultRouter()
router.register('cardapio', CardapioViewSet, basename='Cardapio')
router.register('registro', RegistroViewSet, basename='Registro')
router.register('pedido', PedidoViewSet, basename='Pedido')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('faturamento/', faturamento, name='faturamento'),
    path('api-auth/', include('rest_framework.urls'))
]
