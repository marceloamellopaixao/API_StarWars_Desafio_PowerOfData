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