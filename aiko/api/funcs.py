"""Modulo contendo algumas funcoes extras que foram implementadas
ao longo da API."""

import numpy as np

def get_idx(slug):
    """Funcao que mapeia um indice i ao slug passado a url em um
    processo de HTTP request."""

    if slug == 'veiculos':
        i = 0
    elif slug == 'linhas':
        i = 1
    elif slug == 'paradas':
        i = 2
    elif slug == 'posicaoveiculos':
        i = 3
    else:
        i = -1
    return i

def calculate_distance(objects, lat, lon, n_paradas=3):
    """Funcao de calculo da distancia das paradas dado uma coordenada
    em latitude e longitude. Ela retorna a os id's das n_paradas mais
    proximas, bem como a distancia em numpy.array."""

    objects_num = objects.values_list()
    objects_np = np.array(list(objects_num))
    objects_lat, objects_lon = objects_np[:][:, 2].astype(int), objects_np[:][:, 3].astype(int)

    distance = np.sqrt((lat-objects_lat)**2+(lon-objects_lon)**2)

    args = distance.argsort()[:n_paradas]

    ids_min = objects_np[args][:, 0]

    return ids_min, distance[args]
