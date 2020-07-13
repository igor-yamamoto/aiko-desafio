from django.urls import include, path
from rest_framework import routers
from api import views

# router = routers.DefaultRouter()

urlpatterns = [
    #path('api/veiculos/', views.veiculo_list),
    #path('api/veiculos/id:<int:pk>/', views.veiculo_detail),
    #path('api/linhas/', views.linha_list),
    #path('api/linhas/id:<int:pk>/', views.linha_detail),
    path('linhasporparada/id:<int:parada_id>/', views.linhas_por_parada),
    path('<str:slug>/', views.operate_list),
    path('<str:slug>/id:<int:pk>/', views.operate_details),
]
