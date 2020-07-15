from django.urls import include, path
from rest_framework import routers
from api import views

# router = routers.DefaultRouter()

urlpatterns = [
    path('paradasposicao/<int:lat>:<int:lon>/n:<int:n>/', views.paradas_por_posicao_n),
    path('paradasposicao/<int:lat>:<int:lon>/', views.paradas_por_posicao),
    path('linhasveiculos/', views.veiculos_por_linha_list),
    path('linhasveiculos/id:<int:linha_id>/', views.veiculos_por_linha_detail),
    path('paradaslinhas/', views.linhas_por_parada_list),
    path('paradaslinhas/id:<int:parada_id>/', views.linhas_por_parada_detail),
    path('<str:slug>/', views.operate_list),
    path('<str:slug>/id:<int:pk>/', views.operate_details),
]
