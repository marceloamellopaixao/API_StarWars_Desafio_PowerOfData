from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from api.utils import search_data, get_filter_sorted_data, get_statistics_func

planets = Blueprint('planets', __name__)

@planets.route('/planets', methods=['GET'])
@jwt_required()
def get_planets():
    search_params = {
        'name': request.args.get('name', ''),
        'terrain': request.args.get('terrain', ''),
        'climate': request.args.get('climate', '')
    }

    sort_params = {
        'sort_by': request.args.get('sort_by', 'name'),
        'sort_order': request.args.get('sort_order', 'asc')
    }

    try:
        response = get_filter_sorted_data(search_data, 'planets/', search_params, sort_params)
        return jsonify(response)
    except Exception as e:
        return jsonify({'Erro reconhecido': str(e)}), 404

@planets.route('/planets/statistics', methods=['GET'])
@jwt_required()
def get_planets_statistics():
    planets_data = search_data('planets/')
    planets_list = planets_data.get('results', [])
    total_planets = len(planets_list)

    try:
        countability_atributos = ['terrain', 'climate']
        response = get_statistics_func(planets_list, countability_atributos)

        countability_terrain = response['terrain']
        countability_climate = response['climate']

        return jsonify({
            'Total de Planetas': total_planets,
            'Distribuicao de Terrenos': countability_terrain,
            'Distribuicao de Climas': countability_climate
        })
    except Exception as e:
        return jsonify({'Erro reconhecido': str(e)}), 404

@planets.route('/planets/<int:planet_id>/residents', methods=['GET'])
@jwt_required()
def get_residents_by_planets(planet_id):
    planets_data = search_data(f'planets/{planet_id}/')

    # Verifica se result é um tuple e extrai os dados ou retorna erro
    if isinstance(planets_data, tuple):
        msg, status_code = planets_data
        return jsonify({'msg': msg}), status_code

    film_data = planets_data
    resident_urls = film_data.get('residents', [])

    print(f"URLs dos residentes para o planeta {planet_id}: {resident_urls}")

    return jsonify({'residents': resident_urls}), 200