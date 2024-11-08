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