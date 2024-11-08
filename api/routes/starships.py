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