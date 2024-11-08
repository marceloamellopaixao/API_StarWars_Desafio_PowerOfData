from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from api.utils import search_data, get_filter_sorted_data, get_statistics_func

planets = Blueprint('planets', __name__)

@planets.route('/planets', methods=['GET'])
@jwt_required()
def get_planets():
    """Obtém todos os planetas e filtragem
    ---
    tags:
      - Planetas
    parameters:
      - name: name
        in: query
        type: string
        required: false
        description: Nome do planeta a ser filtrado.
      - name: terrain
        in: query
        type: string
        required: false
        description: Terreno do planeta a ser filtrado.
      - name: climate
        in: query
        type: string
        required: false
        description: Clima do planeta a ser filtrado.
      - name: sort_by
        in: query
        type: string
        required: false
        description: Campo pelo qual classificar os planetas, exemplo - name, terrain e outros.
      - name: sort_order
        in: query
        type: string
        required: false
        description: Ordem da classificação. Pode ser 'asc' para ascendente e 'desc' para descendente.
    responses:
      200:
        description: Lista de planetas filtrados.
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
                    description: Nome do planeta.
                  terrain:
                    type: string
                    description: Terreno do planeta.
                  climate:
                    type: string
                    description: Clima do planeta.
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
    """Obtém estatísticas de planetas
    ---
    tags:
      - Planetas
    description: Retorna estatísticas sobre os planetas disponíveis na API, incluindo contagem total, distribuição de terrenos e climas.
    responses:
      200:
        description: Estatísticas dos planetas.
        schema:
          type: object
          properties:
            Total de Planetas:
              type: integer
              description: Total de planetas disponíveis.
            Distribuição de Terrenos:
              type: object
              additionalProperties:
                type: integer
                description: Contagem de planetas por terrenos.
            Distribuição de Climas:
              type: object
              additionalProperties:
                type: integer
                description: Contagem de planetas por climas.
      404:
        description: Nenhum dado encontrado ou erro durante a busca.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensagem de erro retornada.
    """
    planets = search_data('planets/')
    planets_list = planets.get('results', [])
    total_planets = len(planets_list)

    try:
        contabilizar_atributos = ['terrain', 'climate']
        response = get_statistics_func(planets_list, contabilizar_atributos)

        contabilizador_terrain = response['terrain']
        contabilizador_climate = response['climate']

        return jsonify({
            'Total de Planetas': total_planets,
            'Distribuicao de Terrenos': contabilizador_terrain,
            'Distribuicao de Climas': contabilizador_climate
        })
    except Exception as e:
        return jsonify({'Erro reconhecido': str(e)}), 404