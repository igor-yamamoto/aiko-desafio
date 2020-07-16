"""Arquivo onde sao definidas as views (metodos) para acesso dos dados
contidos nas tabelas. Eles sao distribuidos dentre os 4 metodos pedido
pelo desafio (POST, GET, PUT e DELETE), alem de um adicional para
insercao de dados em campos sem ter que atualizar toda a isntancia
(PATCH).
Os metodos definidos aqui sao:

    - operate_list: metodo que suporta operacoes de POST, GET e DELETE
        para TODAS as instancias de um dado modelo. Dentre os modelos:
        Veiculos, Linha, Paradas, PosicaoVeiculos.

    - operate_details: metodo que suporta operacoes de PUT, GET, PATCH
        e DELETE sobre uma instancia de um dado modelo quando fornecido
        o id (pk). Os modelos sao os mesmos para o caso da `operate_list`.

    - linhas_por_parada_list: metodo que suporta apenas a operacao GET.
        Ela retorna a lista de todas as paradas, apresentando nelas tambem
        uma lista contento todas as linhas associadas as paradas.

    - linhas_por_parada_detail: metodo que suporta as operacoes GET, PUT
        e PATCH. Retorna, quando fornecido o id de uma parada, a instancia
        de uma parada, contendo tambem uma lista com as linhas associadas.

    - veiculos_por_linha_list: metodo que suporta apenas operacoes GET.
        Retorna a lista de todas as linhas, apresentando nelas tambem
        uma lista de todos os veiculos associados a cada linha.

    - veiculos_por_linha_detail: metodo que suporta as operacoes GET, PUT
        e PATCH. Retorna, quando fornecido o id de uma linha, a isntancia
        da linha, contendo tambem uma lista com os veiculos associados.

    - paradas_por_posicao: metodo que suporta apenas a operacao GET.
        Retorna as tres paradas mais proximas da latitude e longitude
        fornecidas como entrada.

    - paradas_por_posicao_n: metodo que suporta apenas a operacao GET.
        Retorna as N paradas mais proximas da latitude e longitude
        fornecidas como entrada.

"""

from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.request import Request
from rest_framework.decorators import api_view

from .serializers import (VeiculoSerializer, LinhaSerializer,
                          ParadasSerializer, PosicaoVeiculosSerializer,
                          LinhasParadaSerializer, VeiculosLinhaSerializer)
from .models import Veiculo, Linha, Paradas, PosicaoVeiculos

from .funcs import get_idx, calculate_distance

models = [Veiculo, Linha, Paradas, PosicaoVeiculos]
serializers = [VeiculoSerializer, LinhaSerializer, ParadasSerializer, PosicaoVeiculosSerializer]
name_models = ['name_veiculo', 'name_linha', 'name_parada']

@api_view(['GET', 'POST', 'DELETE'])
def operate_list(request, modelo):
    """Metodo para apresentar uma lista dos modelos suportados
    (Paradas, Linhas, Veiculos e PosicaoVeiculos). Aqui, o campo
    "modelo" deve ser preenchido com:
        - veiculos: acesso à lista de veiculos registrados
        - linhas: acesso à lista de linhas registradas
        - paradas: acesso à lista de paradas registradas
        - posicaoveiculos: acesso à lista de posição dos veiculos
    """

    i = get_idx(modelo)

    if i == -1:
        return JsonResponse(
            {'message': 'url nao existe dentro da API. Favor, inserir uma dentre as urls possiveis',
             'urls': {'Veiculos': '/api/veiculos/',
                      'Linhas': '/api/linhas/',
                      'Paradas': '/api/paradas/',
                      'Posicao dos veiculos': '/api/posicaoveiculos/',
                      'Relacao de linhas por parada': '/api/paradaslinhas/',
                      'Relacao de veiculos por linhas':'/api/linhasveiculos/',
                      'Posicao das paradas proximas': '/api/linhasveiculos/'}
            })

    model = models[i]
    serializer = serializers[i]

    if request.method == 'GET':
        instance = model.objects.all()
        if i in [3]:
            instance_serializer = serializer(instance, many=True)
        else:
            name_model = name_models[i]
            name_instance = request.GET.get(name_model, None)

            if name_instance is not None:
                instance = instance.filter(name_instance__icontains=name_instance)

        instance_serializer = serializer(instance, many=True)
        return JsonResponse(instance_serializer.data, safe=False)

    if request.method == 'POST':
        instance_data = JSONParser().parse(request)
        instance_serializer = serializer(data=instance_data)

        if instance_serializer.is_valid():
            instance_serializer.save()
            return JsonResponse(instance_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(instance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        instance = model.objects.all()
        instance.delete()
        return JsonResponse({'message': 'Instancia excluida'},
                            status=status.HTTP_204_NO_CONTENT, safe=False)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def operate_details(request, modelo, primary_key):
    """Metodo apra apresentar uma instancia de cada modelo suportado
    (Paradas, Linhas, Veiculos e PosicaoVeiculos). Aqui, o campo
    "modelo" deve ser preenchido com:
        - veiculos: acesso à lista de veiculos registrados
        - linhas: acesso à lista de linhas registradas
        - paradas: acesso à lista de paradas registradas
        - posicaoveiculos: acesso à lista de posição dos veiculos

    """

    i = get_idx(modelo)

    if i == -1:
        return JsonResponse(
            {'message': 'url nao existe dentro da API. Favor, inserir uma dentre as urls possiveis',
             'urls': {'Veiculos': '/api/veiculos/id:{}'.format(primary_key),
                      'Linhas': '/api/linhas/id:{}'.format(primary_key),
                      'Paradas': '/api/paradas/id:{}'.format(primary_key),
                      'Posicao dos veiculos': '/api/posicaoveiculos/id:{}'.format(primary_key),
                      'Relacao de linhas por parada': '/api/paradaslinhas/id:{}'.format(primary_key),
                      'Relacao de veiculos por linhas':'/api/linhasveiculos/id:{}'.format(primary_key)}
            })

    model = models[i]
    serializer = serializers[i]

    try:
        instance = model.objects.get(pk=primary_key)
    except model.DoesNotExist:
        return JsonResponse({'message': 'Instancia nao existe'})

    if request.method == 'GET':
        instance_serializer = serializer(instance)
        return JsonResponse(instance_serializer.data)

    if (request.method == 'PUT' or request.method == 'PATCH'):
        instance_data = JSONParser().parse(request)
        if request.method == 'PUT':
            instance_serializer = serializer(instance, data=instance_data)
        elif request.method == 'PATCH':
            instance_serializer = serializer(instance, data=instance_data, partial=True)
        if instance_serializer.is_valid():
            instance_serializer.save()
            return JsonResponse(instance_serializer.data)
        return JsonResponse(instance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        instance.delete()
        return JsonResponse({'message': 'Instancia deletada da base de dados'},
                            status=status.HTTP_204_NO_CONTENT, safe=False)

@api_view(['GET'])
def linhas_por_parada_list(request):
    """Metodo para listar todas as paradas, acompanhadas das linhas
    associadas."""

    parada_linha = Paradas.objects.all()

    parada_linha_serializer = LinhasParadaSerializer(parada_linha, many=True)
    return JsonResponse(parada_linha_serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'PATCH'])
def linhas_por_parada_detail(request, parada_id):
    """Metodo para apresentar uma parada em especifico, apresentando
    também as linhas associadas."""

    try:
        parada_linha = Paradas.objects.filter(id=parada_id)
    except models.DoesNotExist:
        return JsonResponse({'message': 'Parada nao existe'})

    if request.method == 'GET':
        parada_linha_serializer = LinhasParadaSerializer(parada_linha, many=True)
        return JsonResponse(parada_linha_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif (request.method == 'PUT' or request.method == 'PATCH'):
        parada_linha = Paradas.objects.get(id=parada_id)
        parada_linha_data = JSONParser().parse(request)
        if request.method == 'PUT':
            parada_linha_serializer = LinhasParadaSerializer(parada_linha,
                                                             data=parada_linha_data)
        elif request.method == 'PATCH':
            parada_linha_serializer = LinhasParadaSerializer(
                parada_linha, data=parada_linha_data, partial=True)

        if parada_linha_serializer.is_valid():
            parada_linha_serializer.save()
            return JsonResponse(parada_linha_serializer.data)
        return JsonResponse(parada_linha_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def veiculos_por_linha_list(request):
    """Metodo para listar todas as linhas, acompanhadas dos veiculos
    associados."""

    linha_veiculo = Linha.objects.all()

    linha_veiculo_serializer = VeiculosLinhaSerializer(linha_veiculo, many=True)
    return JsonResponse(linha_veiculo_serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'PATCH'])
def veiculos_por_linha_detail(request, linha_id):
    """Metodo para apresentar uma linha em especifico, apresentando
    também os veiculos associados."""

    try:
        linha_veiculo = Linha.objects.filter(id=linha_id)
    except models.DoesNotExist:
        return JsonResponse({'message': 'Linha nao existe'})

    if request.method == 'GET':
        linha_veiculo_serializer = VeiculosLinhaSerializer(linha_veiculo, many=True)
        return JsonResponse(linha_veiculo_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif (request.method == 'PUT' or request.method == 'PATCH'):
        linha_veiculo = Linha.objects.get(id=linha_id)
        linha_veiculo_data = JSONParser().parse(request)
        if request.method == 'PUT':
            linha_veiculo_serializer = VeiculosLinhaSerializer(
                linha_veiculo, data=linha_veiculo_data)
        elif request.method == 'PATCH':
            linha_veiculo_serializer = VeiculosLinhaSerializer(
                linha_veiculo, data=linha_veiculo_data, partial=True)

        if linha_veiculo_serializer.is_valid():
            linha_veiculo_serializer.save()
            return JsonResponse(linha_veiculo_serializer.data)
        return JsonResponse(linha_veiculo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def paradas_por_posicao(request, lat, lon):
    """Metodo que retorna as tres paradas mais proximas, dadas as
    latitudes e longitudes."""

    lat, lon = int(lat), int(lon)
    print(lat)

    paradas = Paradas.objects.all()

    ids, distances = calculate_distance(paradas, lat, lon)

    paradas = Paradas.objects.filter(id__in=ids)

    paradas_posicao_serializer = ParadasSerializer(paradas, many=True)

    return JsonResponse(paradas_posicao_serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
def paradas_por_posicao_n(request, lat, lon, n_paradas):
    """Metodo que retorna as N paradas mais proximas, dada a
    latitude e longitude."""

    paradas = Paradas.objects.all()

    ids = calculate_distance(paradas, lat, lon, n_paradas)

    paradas = Paradas.objects.filter(id__in=ids)

    paradas_posicao_serializer = ParadasSerializer(paradas, many=True)

    return JsonResponse(paradas_posicao_serializer.data, safe=False, status=status.HTTP_200_OK)
