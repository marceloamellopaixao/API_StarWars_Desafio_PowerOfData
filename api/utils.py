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