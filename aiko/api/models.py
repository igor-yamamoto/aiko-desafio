from django.db import models

class Paradas(models.Model):
    name_parada = models.CharField(max_length = 50, blank = False, default = '')
    lat_parada = models.BigIntegerField(blank = False)
    long_parada = models.BigIntegerField(blank = False)

    def __str__(self):
        return self.name_parada

class Linha(models.Model):
    name_linha = models.CharField(max_length = 50, blank = False, default = '')
    paradas = models.ManyToManyField('Paradas', related_name = 'linhas', blank = True)

    def __str__(self):
        return self.name_linha

class Veiculo(models.Model):
    name_veiculo = models.CharField(max_length = 30, blank = False, default = '')
    model_veiculo = models.CharField(max_length = 30, blank = False, default = '')
    linha = models.ForeignKey('Linha', related_name = 'veiculos', on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return self.name_veiculo

class PosicaoVeiculos(models.Model):
    lat_veiculo = models.BigIntegerField(blank = True)
    long_veiculo = models.BigIntegerField(blank = True)
    veiculo = models.OneToOneField('Veiculo', related_name = 'posicao', on_delete = models.CASCADE, primary_key = True)
