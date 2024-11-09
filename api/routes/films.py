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
        description: Campo pelo qual classificar os filmes, exemplo - title, produtor e diretor.
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
    description: Retorna estatísticas sobre os filmes disponíveis na API, incluindo contagem total, distribuição de produtor e diretor.
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
    films_data = search_data('films/')
    films_list = films_data.get('results', [])
    total_films = len(films_list)

    try:
        countability_attributes = ['producer', 'director']
        response = get_statistics_func(films_list, countability_attributes)

        countability_producer = response['producer']
        countability_director = response['director']

        return jsonify({
            'Total de Personagens': total_films,
            'Distribuicao de Produtores': countability_producer,
            'Distribuicao de Diretores': countability_director
        })
    except Exception as e:
        return jsonify({'Erro reconhecido': str(e)}), 404

@films.route('/films/<int:film_id>/characters', methods=['GET'])
@jwt_required()
def get_characters_by_film(film_id):
    """Obtém personagens de um filme específico
    ---
    tags:
      - Filmes
    parameters:
      - name: film_id
        in: path
        type: integer
        required: true
        description: ID do filme para buscar os personagens.
    responses:
      200:
        description: Lista de URLs dos personagens do filme.
        schema:
          type: object
          properties:
            characters:
              type: array
              items:
                type: string
                description: URL do personagem na API.
      404:
        description: Filme não encontrado ou sem personagens.
        schema:
          type: object
          properties:
            msg:
              type: string
              description: Mensagem de erro retornada.
    """
    result = search_data(f'films/{film_id}/')

    # Verifica se result é um tuple e extrai os dados ou retorna erro
    if isinstance(result, tuple):
        msg, status_code = result
        return jsonify({'msg': msg}), status_code

    film_data = result
    character_urls = film_data.get('characters', [])

    print(f"URLs dos personagens para o filme {film_id}: {character_urls}")

    return jsonify({'characters': character_urls}), 200