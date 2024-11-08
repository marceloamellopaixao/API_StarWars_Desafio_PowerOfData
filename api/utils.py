import requests

# Função para buscar os dados na api
SWAPI_URL = 'https://swapi.dev/api/'
def search_data(endpoint):
    response = requests.get(SWAPI_URL + endpoint)
    try:
        if response.status_code == 200:
            return response.json()
        else:
            return {'Erro reconhecido': 'Dado não encontrado'}, response.status_code
    except Exception as e:
        return {'Erro reconhecido': str(e)}, response.status_code


# Função de Filtragem dos Dados
def filter_data(data_list, **search_params):
    """Filtra a lista de dados de acordo com os critérios de pesquisa.

    Args:
        data_list (list): A lista de dados a ser filtrada.
        search_params (dict): Parâmetros de pesquisa.

    Returns:
        list: A lista filtrada.
    """
    filtered_data = []
    for item in data_list:
        match = True
        for key, value in search_params.items():
            if value and value.lower() not in str(item.get(key, '')).lower():
                match = False
                break
        if match:
            filtered_data.append(item)
    return filtered_data


# Função de Ordenação dos Dados
def sort_data(data_list, sort_by='name', sort_order='asc'):
    """Classifica a lista de dados de acordo com o campo e ordem especificados.

    Args:
        data_list (list): A lista de dados a ser classificada.
        sort_by (str): O campo pelo qual classificar.
        sort_order (str): A ordem da classificação ('asc' ou 'desc').

    Returns:
        list: A lista classificada.
    """
    return sorted(data_list, key=lambda x: x[sort_by], reverse=(sort_order == 'desc'))


# Função de Filtro e Ordenação
def get_filter_sorted_data(search_data_func, endpoint, search_params=None, sort_params=None):
    """Função genérica para obter, filtrar e classificar dados de um endpoint.

    Args:
        search_data_func (function): A função que busca os dados do endpoint.
        endpoint (str): O endpoint do qual obter os dados.
        search_params (dict, optional): Um dicionário com os parâmetros de pesquisa.
        sort_params (dict, optional): Um dicionário com os parâmetros de classificação.

    Returns:
        dict: Um dicionário contendo os dados filtrados e classificados.
    """
    # Inicializa os parâmetros de pesquisa e classificação
    if search_params is None:
        search_params = {}

    if sort_params is None:
        sort_params = {
            'sort_by': '',
            'sort_order': 'asc'
        }

    # Busca os dados do endpoint
    data = search_data_func(endpoint)
    data_list = data.get('results', [])

    # Filtra os dados usando os parâmetros de pesquisa
    filtered_data = filter_data(data_list, **search_params)

    # Obtém os parâmetros de classificação
    sort_by = sort_params.get('sort_by', '')
    sort_order = sort_params.get('sort_order', 'asc')

    # Classifica os dados filtrados
    sorted_data = sort_data(filtered_data, sort_by, sort_order)

    return {'results': sorted_data}

# Função de Estatísticas
def get_statistics_func(data_list, atributos):
    """
    Conta a ocorrência de atributos específicos em uma lista de dicionários.

    :param data_list: Lista de dicionários contendo os dados a serem analisados.
    :param atributos: Lista de atributos cujas ocorrências devem ser contadas.
    :return: Dicionário com a contagem de cada atributo.
    """

    contagem = {atributo: {} for atributo in atributos}

    for item in data_list:
        for atributo in atributos:
            valor = item.get(atributo)
            if valor:
                if valor in contagem[atributo]:
                    contagem[atributo][valor] += 1
                else:
                    contagem[atributo][valor] = 1

    return contagem

