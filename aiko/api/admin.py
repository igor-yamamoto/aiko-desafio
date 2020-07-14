from django.contrib import admin
from .models import Veiculo, Linha, Paradas, PosicaoVeiculos

models_list = [Veiculo, Linha, Paradas, PosicaoVeiculos]

admin.site.register(models_list)
