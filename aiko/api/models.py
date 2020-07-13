from django.db import models

class Veiculo(models.Model):
    name_veiculo = models.CharField(max_length = 30, blank = False, default = '')
    model_veiculo = models.CharField(max_length = 30, blank = False, default = '')
    linha = models.ForeignKey('Linha', on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return self.name_veiculo

class Linha(models.Model):
    name_linha = models.CharField(max_length = 50, blank = False, default = '')

    def __str__(self):
        return self.name_linha

class Paradas(models.Model):
    name_parada = models.CharField(max_length = 50, blank = False, default = '')
    lat_parada = models.BigIntegerField()
    long_parada = models.BigIntegerField()

    def __str__(self):
        return self.name_parada

class ParadasLinha(models.Model):
    linha = models.ForeignKey('Linha', on_delete = models.CASCADE, null = True)
    paradas = models.ForeignKey('Paradas', on_delete = models.CASCADE, null = True)

class PosicaoVeiculos(models.Model):
    lat_veiculo = models.BigIntegerField()
    long_veiculo = models.BigIntegerField()
    veiculo = models.ForeignKey('Veiculo', on_delete = models.CASCADE, null = True)
