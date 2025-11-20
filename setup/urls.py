from django.contrib import admin
from django.urls import path, include
from app.views import CardapioViewSet, RegistroViewSet, PedidoViewSet, faturamento, MetodoPagamentoViewSet
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


# Criação das rotas automáticas
router = routers.DefaultRouter()
router.register('cardapio', CardapioViewSet, basename='Cardapio')
router.register('registro', RegistroViewSet, basename='Registro')
router.register('pedido', PedidoViewSet, basename='Pedido')
router.register('metodos-pagamento', MetodoPagamentoViewSet,
                basename='metodos-pagamento')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    # Autenticação via JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Rota de faturamento
    path('faturamento/', faturamento, name='faturamento'),
    # Login do DRF
    path('api-auth/', include('rest_framework.urls')),
    # Documentação da API (Swagger)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
]
