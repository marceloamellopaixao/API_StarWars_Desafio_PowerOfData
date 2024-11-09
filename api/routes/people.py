from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from api.utils import search_data, get_filter_sorted_data, get_statistics_func

people = Blueprint('people', __name__)

@people.route('/people', methods=['GET'])
@jwt_required()
def get_people():
    """Obtém todos os personagens filtrados
    ---
    tags:
      - Personagens
    parameters:
      - name: name
        in: query
        type: string
        required: false
        description: Nome da Personagem a ser filtrada.
      - name: gender
        in: query
        type: string
        required: false
        description: Gênero da Personagem a ser filtrada.
      - name: hair_color
        in: query
        type: string
        required: false
        description: Cor do cabelo da Personagem a ser filtrada.
      - name: birth_year
        in: query
        type: string
        required: false
        description: Ano de nascimento da Personagem a ser filtrada.
      - name: sort_by
        in: query
        type: string
        required: false
        description: Campo pelo qual classificar as Personagens, exemplo - name, gender e outros.
      - name: sort_order
        in: query
        type: string
        required: false
        description: Ordem da classificação. Pode ser 'asc' para ascendente e 'desc' para descendente.
    responses:
      200:
        description: Lista de Personagens filtradas.
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
                    description: Nome da Personagem.
                  gender:
                    type: string
                    description: Gênero da Personagem.
                  hair_color:
                    type: string
                    description: Cor do cabelo da Personagem.
                  birth_year:
                    type: string
                    description: Ano de nascimento da Personagem.
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
    """Obtém estatísticas de personagens
    ---
    tags:
      - Personagens
    description: Retorna estatísticas sobre os personagens disponíveis na API, incluindo contagem total, distribuição de gênero, cor do cabelo e ano de nascimento.
    responses:
      200:
        description: Estatísticas dos personagens.
        schema:
          type: object
          properties:
            Total de Personagens:
              type: integer
              description: Total de personagens disponíveis.
            Distribuição de Gêneros:
              type: object
              additionalProperties:
                type: integer
                description: Contagem de personagens por gênero.
            Distribuição de Cores de Cabelo:
              type: object
              additionalProperties:
                type: integer
                description: Contagem de personagens por cor de cabelo.
            Distribuição de Anos de Nascimento:
              type: object
              additionalProperties:
                type: integer
                description: Contagem de personagens por ano de nascimento.
      404:
        description: Nenhum dado encontrado ou erro durante a busca.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensagem de erro retornada.
    """
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
    """Obtém o planeta natal de um(a) personagem específico(a)
    ---
    tags:
      - Personagens
    parameters:
      - name: people_id
        in: path
        type: integer
        required: true
        description: ID do personagem para buscar o planeta natal.
    responses:
      200:
        description: URL do planeta natal do personagem.
        schema:
          type: object
          properties:
            homeworld:
              type: string
              description: URL do planeta natal na API.
      404:
        description: Personagem não encontrado ou sem planeta natal.
        schema:
          type: object
          properties:
            msg:
              type: string
              description: Mensagem de erro retornada.
    """
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