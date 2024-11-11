from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from api.utils import search_data, get_filter_sorted_data, get_statistics_func

films = Blueprint('films', __name__)

@films.route('/films', methods=['GET'])
@jwt_required()
def get_films():
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
    result = search_data(f'films/{film_id}/')

    # Verifica se result é um tuple e extrai os dados ou retorna erro
    if isinstance(result, tuple):
        msg, status_code = result
        return jsonify({'msg': msg}), status_code

    film_data = result
    character_urls = film_data.get('characters', [])

    print(f"URLs dos personagens para o filme {film_id}: {character_urls}")

    return jsonify({'characters': character_urls}), 200
