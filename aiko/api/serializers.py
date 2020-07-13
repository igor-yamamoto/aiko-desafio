from rest_framework import serializers
from .models import Veiculo, Linha, Paradas, ParadasLinha, PosicaoVeiculos

class VeiculoSerializer(serializers.HyperlinkedModelSerializer):
    linha_id = serializers.IntegerField()

    class Meta:
        model = Veiculo
        #fields = ('id', 'name_veiculo', 'model_veiculo')
        fields = ['id', 'name_veiculo', 'model_veiculo', 'linha_id']

class LinhaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Linha
        fields = ['id', 'name_linha']

class ParadasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Paradas
        fields = ['id', 'name_parada', 'lat_parada', 'long_parada']

class ParadasLinhaSerializer(serializers.HyperlinkedModelSerializer):
    linha_id = serializers.IntegerField()
    paradas_id = serializers.IntegerField()

    class Meta:
        model = ParadasLinha
        fields = ['id', 'linha_id', 'paradas_id']

class PosicaoVeiculosSerializer(serializers.HyperlinkedModelSerializer):
    veiculo_id = serializers.IntegerField()

    class Meta:
        model = PosicaoVeiculos
        fields = ['id', 'lat_veiculo', 'long_veiculo', 'veiculo_id']


class LinhasPorParadaSerializer(serializers.Serializer):
    linha_id = serializers.IntegerField()
    paradas_id = serializers.IntegerField()

    class Meta:
        model = ParadasLinha
        fields = ['paradas_id', 'linha_id']
