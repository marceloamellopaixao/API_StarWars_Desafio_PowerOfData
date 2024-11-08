from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from api.utils import load_users, save_users

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    """Registra um novo usuário
    ---
    tags:
      - Autenticação
    parameters:
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Nome de usuário para registro.
              example: "novo_usuario"
            password:
              type: string
              description: Senha do usuário.
              example: "senha123"
          required:
            - username
            - password
    responses:
      201:
        description: Usuário registrado com sucesso.
      400:
        description: Usuário já existe ou erro na requisição.
    """
    data = load_users()
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'msg': 'Usuário ou Senha vazio!'}), 400

    # Verifica se o usuário já existe
    for user in data['users']:
        if user['username'] == username:
            return jsonify({'msg': 'Usuário já existe!'}), 400

    # Adiciona o novo usuário
    new_user = {
        "username": username,
        "password": password  # Lembre-se de usar hashing em produção
    }
    data['users'].append(new_user)

    # Salva os dados no arquivo
    save_users(data)

    return jsonify({'msg': 'Usuário registrado com sucesso!'}), 201