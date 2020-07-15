from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.request import Request

from .serializers import VeiculoSerializer, LinhaSerializer, ParadasSerializer,  PosicaoVeiculosSerializer, LinhasParadaSerializer, VeiculosLinhaSerializer
from .models import Veiculo, Linha, Paradas, PosicaoVeiculos

from rest_framework.decorators import api_view

from .funcs import get_idx, calculate_distance

models = [Veiculo, Linha, Paradas, PosicaoVeiculos]
serializers = [VeiculoSerializer, LinhaSerializer, ParadasSerializer, PosicaoVeiculosSerializer]
name_models = ['name_veiculo', 'name_linha', 'name_parada']

@api_view(['GET', 'POST', 'DELETE'])
def operate_list(request, slug):
    i = get_idx(slug)

    model = models[i]
    serializer = serializers[i]

    if request.method == 'GET':
        instance = model.objects.all()
        if i in [3]:
            instance_serializer = serializer(instance, many = True)
        else:
            name_model = name_models[i]
            name_instance = request.GET.get(name_model, None)

            if name_instance is not None:
                instance = instance.filter(name_instance__icontains = name_instance)

        instance_serializer = serializer(instance, many = True)
        return JsonResponse(instance_serializer.data, safe = False)

    elif request.method == 'POST':
        instance_data = JSONParser().parse(request)
        instance_serializer = serializer(data = instance_data)

        if instance_serializer.is_valid():
            instance_serializer.save()
            return JsonResponse(instance_serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(instance_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        instance = model.objects.all()
        instance.delete()
        return JsonResponse({'message': 'Instancia excluida'}, status = status.HTTP_204_NO_CONTENT, safe = False)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def operate_details(request, slug, pk):
    i = get_idx(slug)

    model = models[i]
    serializer = serializers[i]

    try:
        instance = model.objects.get(pk = pk)
    except model.DoesNotExist:
        return JsonResponse({'message': 'Instancia nao existe'})

    if request.method == 'GET':
        instance_serializer = serializer(instance)
        return JsonResponse(instance_serializer.data)

    elif (request.method == 'PUT' or request.method == 'PATCH'):
        instance_data = JSONParser().parse(request)
        if request.method == 'PUT':
            instance_serializer = serializer(instance, data = instance_data)
        if request.method == 'PATCH':
            instance_serializer = serializer(instance, data = instance_data, partial = True)
        if instance_serializer.is_valid():
            instance_serializer.save()
            return JsonResponse(instance_serializer.data)
        return JsonResponse(instance_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        instance.delete()
        return JsonResponse({'message': 'Instancia deletada da base de dados'}, status = status.HTTP_204_NO_CONTENT, safe = False)

@api_view(['GET'])
def linhas_por_parada_list(request):
    parada_linha = Paradas.objects.all()

    parada_linha_serializer = LinhasParadaSerializer(parada_linha, many = True)
    return JsonResponse(parada_linha_serializer.data, safe = False, status = status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'PATCH'])
def linhas_por_parada_detail(request, parada_id):
    try:
        parada_linha = Paradas.objects.filter(id=parada_id)
    except:
        return JsonResponse({'message': 'Parada nao existe'})

    if request.method == 'GET':
        parada_linha_serializer = LinhasParadaSerializer(parada_linha, many = True)
        return JsonResponse(parada_linha_serializer.data, safe = False, status = status.HTTP_200_OK)

    elif (request.method == 'PUT' or request.method == 'PATCH'):
        parada_linha = Paradas.objects.get(id = parada_id)
        parada_linha_data = JSONParser().parse(request)
        if request.method == 'PUT':
            parada_linha_serializer = LinhasParadaSerializer(parada_linha, data = parada_linha_data)
        elif request.method == 'PATCH':
            parada_linha_serializer = LinhasParadaSerializer(parada_linha, data = parada_linha_data, partial = True)

        if parada_linha_serializer.is_valid():
            parada_linha_serializer.save()
            return JsonResponse(parada_linha_serializer.data)
        return JsonResponse(parada_linha_serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def veiculos_por_linha_list(request):
    linha_veiculo = Linha.objects.all()

    linha_veiculo_serializer = VeiculosLinhaSerializer(linha_veiculo, many = True)
    return JsonResponse(linha_veiculo_serializer.data, safe = False, status = status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'PATCH'])
def veiculos_por_linha_detail(request, linha_id):
    try:
        linha_veiculo = Linha.objects.filter(id=linha_id)
    except model.DoesNotExist:
        return JsonResponse({'message': 'Linha nao existe'})

    if request.method == 'GET':
        linha_veiculo_serializer = VeiculosLinhaSerializer(linha_veiculo, many = True)
        return JsonResponse(linha_veiculo_serializer.data, safe = False, status = status.HTTP_200_OK)

    elif (request.method == 'PUT' or request.method == 'PATCH'):
        linha_veiculo = Linha.objects.get(id = linha_id)
        linha_veiculo_data = JSONParser().parse(request)
        if request.method == 'PUT':
            linha_veiculo_serializer = VeiculosLinhaSerializer(linha_veiculo, data = linha_veiculo_data)
        elif request.method == 'PATCH':
            linha_veiculo_serializer = VeiculosLinhaSerializer(linha_veiculo, data = linha_veiculo_data, partial = True)

        if linha_veiculo_serializer.is_valid():
            linha_veiculo_serializer.save()
            return JsonResponse(linha_veiculo_serializer.data)
        return JsonResponse(linha_veiculo_serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def paradas_por_posicao(request, lat, lon):
    import numpy as np

    paradas = Paradas.objects.all()

    ids, distances = calculate_distance(paradas, lat, lon, 3)

    paradas = Paradas.objects.filter(id__in = ids)

    paradas_posicao_serializer = ParadasSerializer(paradas, many = True)

    return JsonResponse(paradas_posicao_serializer.data, safe = False, status = status.HTTP_200_OK)


@api_view(['GET'])
def paradas_por_posicao_n(request, lat, lon, n):
    import numpy as np

    paradas = Paradas.objects.all()

    ids, distances = calculate_distance(paradas, lat, lon, n)

    paradas = Paradas.objects.filter(id__in = ids)

    paradas_posicao_serializer = ParadasSerializer(paradas, many = True)

    return JsonResponse(paradas_posicao_serializer.data, safe = False, status = status.HTTP_200_OK)
