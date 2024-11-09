from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from api.utils import search_data, get_filter_sorted_data, get_statistics_func

starships = Blueprint('starships', __name__)

@starships.route('/starships', methods=['GET'])
@jwt_required()
def get_starships():
    """Obtém todas as naves estelares
    ---
    tags:
      - Naves Estelares
    parameters:
      - name: name
        in: query
        type: string
        required: false
        description: Nome da nave estelar a ser filtrada.
      - name: manufacturer
        in: query
        type: string
        required: false
        description: Fabricante da nave estelar a ser filtrada.
      - name: starship_class
        in: query
        type: string
        required: false
        description: Classe da nave estelar a ser filtrada.
      - name: sort_by
        in: query
        type: string
        required: false
        description: Campo pelo qual classificar as naves estelares, exemplo - name, manufacturer e outros.
      - name: sort_order
        in: query
        type: string
        required: false
        description: Ordem da classificação. Pode ser 'asc' para ascendente e 'desc' para descendente.
    responses:
      200:
        description: Lista de naves estelares filtradas.
        schema:
          type: object
          properties:
            results:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                    description: Nome da nave estelar.
                  manufacturer:
                    type: string
                    description: Fabricante da nave estelar.
                  starship_class:
                    type: string
                    description: Classe da nave estelar.
      404:
        description: Nenhum resultado encontrado.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensagem de erro retornada.
    """
    search_params = {
        'name': request.args.get('name', ''),
        'manufacturer': request.args.get('manufacturer', ''),
        'starship_class': request.args.get('starship_class', '')
    }

    sort_params = {
        'sort_by': request.args.get('sort_by', 'name'),
        'sort_order': request.args.get('sort_order', 'asc')
    }

    try:
        response = get_filter_sorted_data(search_data, 'starships/', search_params, sort_params)
        return jsonify(response)
    except Exception as e:
        return jsonify({'Erro reconhecido': str(e)}), 404


@starships.route('/starships/statistics', methods=['GET'])
@jwt_required()
def get_starships_statistics():
    """Obtém estatísticas de naves estelares
    ---
    tags:
      - Naves Estelares
    description: Retorna estatísticas sobre as naves estelares disponíveis na API, incluindo contagem total, distribuição de fabricantes e classes de naves estelares.
    responses:
      200:
        description: Estatísticas das naves estelares.
        schema:
          type: object
          properties:
            Total de Naves Estelares:
              type: integer
              description: Total de naves estelares disponíveis.
            Distribuição de Fabricantes:
              type: object
              additionalProperties:
                type: integer
                description: Contagem de naves estelares por Fabricantes.
            Distribuição de Classes de Naves Estelares:
              type: object
              additionalProperties:
                type: integer
                description: Contagem de naves estelares por Classes de Naves Estelares.
      404:
        description: Nenhum dado encontrado ou erro durante a busca.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensagem de erro retornada.
    """
    starships_data = search_data('starships/')
    starships_list = starships_data.get('results', [])
    total_starships = len(starships_list)

    try:
        contabilizar_atributos = ['manufacturer', 'starship_class']
        response = get_statistics_func(starships_list, contabilizar_atributos)

        contabilizador_manufacturer = response['manufacturer']
        contabilizador_starship_class = response['starship_class']

        return jsonify({
            'Total de Naves Estelares': total_starships,
            'Distribuicao de Fabricantes': contabilizador_manufacturer,
            'Distribuicao de Classes de Naves Estelares': contabilizador_starship_class
        })
    except Exception as e:
        return jsonify({'Erro reconhecido': str(e)}), 404

@starships.route('/starships/<int:starship_id>/films', methods=['GET'])
# @jwt_required()
def get_residents_by_planets(starship_id):
    """Obtém os filmes de uma nave estelar específico
    ---
    tags:
      - Naves Estelares
    parameters:
      - name: starship_id
        in: path
        type: integer
        required: true
        description: ID do nave estelar para buscar os filmes.
    responses:
      200:
        description: Lista de URLs dos filmes da nave estelar.
        schema:
          type: object
          properties:
            filmes:
              type: array
              items:
                type: string
                description: URL do filme na API.
      404:
        description: Nave estelar não encontrada ou sem filmes.
        schema:
          type: object
          properties:
            msg:
              type: string
              description: Mensagem de erro retornada.
    """
    starships_data = search_data(f'starships/{starship_id}/')

    # Verifica se result é um tuple e extrai os dados ou retorna erro
    if isinstance(starships_data, tuple):
        msg, status_code = starships_data
        return jsonify({'msg': msg}), status_code

    film_data = starships_data
    films_urls = film_data.get('films', [])

    print(f"URLs dos filmes para a nave estelar {starship_id}: {films_urls}")

    return jsonify({'films': films_urls}), 200