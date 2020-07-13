from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.request import Request

from .serializers import VeiculoSerializer, LinhaSerializer, ParadasSerializer, ParadasLinhaSerializer, PosicaoVeiculosSerializer, LinhasPorParadaSerializer
from .models import Veiculo, Linha, Paradas, ParadasLinha, PosicaoVeiculos

from rest_framework.decorators import api_view

from .funcs import get_idx

models = [Veiculo, Linha, Paradas, ParadasLinha, PosicaoVeiculos]
serializers = [VeiculoSerializer, LinhaSerializer, ParadasSerializer, ParadasLinhaSerializer, PosicaoVeiculosSerializer]
name_models = ['name_veiculo', 'name_linha', 'name_parada']

@api_view(['GET', 'POST', 'DELETE'])
def operate_list(request, slug):
    i = get_idx(slug)

    model = models[i]
    serializer = serializers[i]

    if request.method == 'GET':
        instance = model.objects.all()
        if i in [3, 4]:
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

@api_view(['GET', 'PUT', 'DELETE'])
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

    elif request.method == 'PUT':
        instance_data = JSONParser().parse(request)
        instance_serializer = serializer(instance, data = instance_data)
        if instance_serializer.is_valid():
            instance_serializer.save()
            return JsonResponse(instance_serializer.data)
        return JsonResponse(instance_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        instance.delete()
        return JsonResponse({'message': 'Instancia deletada da base de dados'}, status = status.HTTP_204_NO_CONTENT, safe = False)

@api_view(['GET'])
def linhas_por_parada(request, parada_id):
    try:
        parada_linha = ParadasLinha.objects.filter(paradas_id=parada_id)
    except:
        return JsonResponse({'message': 'Parada nao existe'})

    linha_id_arr = parada_linha.values('linha_id')
    nome_linha = Linha.objects.filter(id__in = linha_id_arr)
    print(nome_linha)
    print(parada_linha)
    parada_linha_serializer = LinhasPorParadaSerializer(parada_linha, many = True)
    return JsonResponse(parada_linha_serializer.data, safe = False, status = status.HTTP_200_OK)

