from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from api.utils import search_data, get_filter_sorted_data, get_statistics_func

people = Blueprint('people', __name__)

@people.route('/people', methods=['GET'])
@jwt_required()
def get_people():
    search_params = {
        'name': request.args.get('name', ''),
        'gender': request.args.get('gender', ''),
        'hair_color': request.args.get('hair_color', ''),
        'birth_year': request.args.get('birth_year', '')
    }

    sort_params = {
        'sort_by': request.args.get('sort_by', 'name'),
        'sort_order': request.args.get('sort_order', 'asc')
    }

    try:
        response = get_filter_sorted_data(search_data, 'people/', search_params, sort_params)
        return jsonify(response)
    except Exception as e:
        return jsonify({'Erro reconhecido': str(e)}), 404

@people.route('/people/statistics', methods=['GET'])
@jwt_required()
def get_people_statistics():
    people_data = search_data('people/')
    people_list = people_data.get('results', [])
    total_people = len(people_list)

    try:
        countability_attributes = ['gender', 'hair_color', 'birth_year']
        response = get_statistics_func(people_list, countability_attributes)

        countability_gender = response['gender']
        countability_hair_color = response['hair_color']
        countability_birth_year = response['birth_year']

        return jsonify({
            'Total de Personagens': total_people,
            'Distribuicao de Generos': countability_gender,
            'Distribuicao de Cores de Cabelo': countability_hair_color,
            'Distribuicao de Ano de Nascimento': countability_birth_year
        })
    except Exception as e:
        return jsonify({'Erro reconhecido': str(e)}), 404

@people.route('/people/<int:people_id>/homeworld', methods=['GET'])
@jwt_required()
def get_homeworld_by_person(people_id):
    result = search_data(f'people/{people_id}/')

    # Verifica se result é um tuple e extrai os dados ou retorna erro
    if isinstance(result, tuple):
        msg, status_code = result
        return jsonify({'msg': msg}), status_code

    people_result = result
    homeworld_url = people_result.get('homeworld')

    # Caso não exista planeta natal, retorne uma mensagem de erro
    if not homeworld_url:
        return jsonify({'msg': 'Planeta natal não encontrado para este personagem.'}), 404

    print(f"URL do planeta natal para o personagem {people_id}: {homeworld_url}")

    return jsonify({'homeworld': homeworld_url}), 200
