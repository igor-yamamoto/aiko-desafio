def get_idx(slug):
    i = 0
    if slug == 'veiculos':
        i = 0
    elif slug == 'linhas':
        i = 1
    elif slug == 'paradas':
        i = 2
    elif slug == 'posicaoveiculos':
        i = 3
    return i

def calculate_distance(objects, lat, lon, n = 1):
    import numpy as np

    objects_num = objects.values_list()
    objects_np = np.array(list(objects_num))
    objects_lat, objects_lon = objects_np[:][:, 2].astype(int), objects_np[:][:, 3].astype(int)

    distance = np.sqrt((lat-objects_lat)**2+(lon-objects_lon)**2)

    args = distance.argsort()[:n]

    ids_min = objects_np[args][:, 0]

    return ids_min, distance[args]
