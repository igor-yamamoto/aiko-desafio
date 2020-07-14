from rest_framework import serializers
from .models import Veiculo, Linha, Paradas, PosicaoVeiculos

class PosicaoVeiculosSerializer(serializers.ModelSerializer):
    veiculo_id = serializers.IntegerField()

    class Meta:
        model = PosicaoVeiculos
        fields = ['lat_veiculo', 'long_veiculo', 'veiculo_id']

class PosicaoVeiculosSimplesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PosicaoVeiculos
        fields = ['lat_veiculo', 'long_veiculo']

class VeiculoSerializer(serializers.ModelSerializer):
    linha_id = serializers.IntegerField()
    posicao = PosicaoVeiculosSimplesSerializer(read_only = True)

    class Meta:
        model = Veiculo
        #fields = ('id', 'name_veiculo', 'model_veiculo')
        fields = ['id', 'name_veiculo', 'model_veiculo', 'linha_id', 'posicao']
        extra_kwargs = {'posicao': {'required': False}}

class VeiculoSimplesSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['id']
        model = Veiculo
        #fields = ('id', 'name_veiculo', 'model_veiculo')
        fields = ['id', 'name_veiculo', 'model_veiculo']

class VeiculosLinhaSerializer(serializers.ModelSerializer):
    veiculos = VeiculoSimplesSerializer(many = True, read_only = True)

    class Meta:
        ordering = ['id']
        model = Linha
        fields = ['id', 'name_linha', 'paradas', 'veiculos']
        extra_kwargs = {'paradas': {'required': False}}
        extra_kwargs = {'veiculos': {'required': False}}

class LinhaSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['id']
        model = Linha
        fields = ['id', 'name_linha', 'paradas']
        extra_kwargs = {'paradas': {'required': False}}

class LinhaSimplesSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['id']
        model = Linha
        fields = ['id', 'name_linha']

class ParadasSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['id']
        model = Paradas
        fields = ['id', 'name_parada', 'lat_parada', 'long_parada']

class LinhasParadaSerializer(serializers.ModelSerializer):
    linhas = LinhaSimplesSerializer(many = True, read_only = True)

    class Meta:
        ordering = ['id']
        model = Paradas
        fields = ['id', 'name_parada', 'lat_parada', 'long_parada', 'linhas']
        extra_kwargs = {'linhas': {'required': False}}
