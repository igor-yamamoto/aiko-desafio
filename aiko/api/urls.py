from django.urls import include, path
from rest_framework import routers
from api import views

# router = routers.DefaultRouter()

urlpatterns = [
    path('linhasveiculos/', views.veiculos_por_linha_list),
    path('linhasveiculos/id:<int:linha_id>/', views.veiculos_por_linha_detail),
    path('paradaslinhas/', views.linhas_por_parada_list),
    path('paradaslinhas/id:<int:parada_id>/', views.linhas_por_parada_detail),
    path('<str:slug>/', views.operate_list),
    path('<str:slug>/id:<int:pk>/', views.operate_details),
]
