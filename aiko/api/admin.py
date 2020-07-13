from django.contrib import admin
from .models import Veiculo, Linha, Paradas, ParadasLinha, PosicaoVeiculos

models_list = [Veiculo, Linha, Paradas, ParadasLinha, PosicaoVeiculos]

admin.site.register(models_list)
