from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from api.utils import search_data, get_filter_sorted_data, get_statistics_func

starships = Blueprint('starships', __name__)

@starships.route('/starships', methods=['GET'])
@jwt_required()
def get_starships():
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
@jwt_required()
def get_films_by_starships(starship_id):
    starships_data = search_data(f'starships/{starship_id}/')

    # Verifica se result é um tuple e extrai os dados ou retorna erro
    if isinstance(starships_data, tuple):
        msg, status_code = starships_data
        return jsonify({'msg': msg}), status_code

    film_data = starships_data
    films_urls = film_data.get('films', [])

    print(f"URLs dos filmes para a nave estelar {starship_id}: {films_urls}")

    return jsonify({'films': films_urls}), 200