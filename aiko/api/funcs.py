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
