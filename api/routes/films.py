from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from api.utils import search_data, get_filter_sorted_data, get_statistics_func

films = Blueprint('films', __name__)

@films.route('/films', methods=['GET'])
@jwt_required()
def get_films():
    """Obtém todos os filmes
    ---
    tags:
      - Filmes
    parameters:
      - name: title
        in: query
        type: string
        required: false
        description: Título do filme para filtrar a lista de filmes.
      - name: producer
        in: query
        type: string
        required: false
        description: Nome do produtor para filtrar a lista de filmes.
      - name: director
        in: query
        type: string
        required: false
        description: Nome do diretor para filtrar a lista de filmes.
      - name: sort_by
        in: query
        type: string
        required: false
        description: Campo pelo qual classificar os filmes, exemplo - title.
      - name: sort_order
        in: query
        type: string
        required: false
        description: Ordem da classificação. Pode ser 'asc' para ascendente e 'desc' para descendente.
    responses:
      200:
        description: Lista de filmes filtrados e classificados.
        schema:
          type: object
          properties:
            results:
              type: array
              items:
                type: object
                properties:
                  title:
                    type: string
                    description: Título do filme.
                  producer:
                    type: string
                    description: Nome do produtor do filme.
                  director:
                    type: string
                    description: Nome do diretor do filme.
                  release_date:
                    type: string
                    description: Data de lançamento do filme.
      404:
        description: Nenhum filme encontrado ou erro durante a busca.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensagem de erro retornada.
    """

    search_params = {
        'title': request.args.get('title', ''),
        'producer': request.args.get('producer', ''),
        'director': request.args.get('director', '')
    }

    sort_params = {
        'sort_by': request.args.get('sort_by', 'title'),
        'sort_order': request.args.get('sort_order', 'asc')
    }

    try:
        response = get_filter_sorted_data(search_data, 'films/', search_params, sort_params)
        return jsonify(response)
    except Exception as e:
        return jsonify({'Erro reconhecido': str(e)}), 404


@films.route('/films/statistics', methods=['GET'])
@jwt_required()
def get_films_statistics():
    """Obtém estatísticas de filmes
    ---
    tags:
      - Filmes
    description: Retorna estatísticas sobre os filmes disponíveis na API, incluindo contagem total, distribuição de produtor e diretor..
    responses:
      200:
        description: Estatísticas dos filmes.
        schema:
          type: object
          properties:
            Total de Filmes:
              type: integer
              description: Total de filmes disponíveis.
            Distribuição de Produtores:
              type: object
              additionalProperties:
                type: integer
                description: Contagem de filmes por produtor.
            Distribuição de Diretores:
              type: object
              additionalProperties:
                type: integer
                description: Contagem de personagens por diretor.
      404:
        description: Nenhum dado encontrado ou erro durante a busca.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensagem de erro retornada.
    """
    films = search_data('films/')
    films_list = films.get('results', [])
    total_films = len(films_list)

    try:
        contabilizar_atributos = ['producer', 'director']
        response = get_statistics_func(films_list, contabilizar_atributos)

        contabilizador_producer = response['producer']
        contabilizador_director = response['director']

        return jsonify({
            'Total de Personagens': total_films,
            'Distribuicao de Produtores': contabilizador_producer,
            'Distribuicao de Diretores': contabilizador_director
        })
    except Exception as e:
        return jsonify({'Erro reconhecido': str(e)}), 404