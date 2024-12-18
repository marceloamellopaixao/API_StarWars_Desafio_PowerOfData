from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from api.utils import load_users, save_users

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    """
    Registra um novo usuário
    """
    data = load_users()

    # Verifica se os dados foram carregados corretamente
    if data is None or 'users' not in data:
        data = {"users": []}  # Se falhar, inicializa com uma lista vazia

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

@auth.route('/login', methods=['POST'])
def login():
    """
    Realiza o login e retorna um token JWT
    """
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'msg': 'Usuário ou Senha vazio!'}), 400

    users = load_users()

    for user in users['users']:
        if user['username'] == username and user['password'] == password:
            access_token = create_access_token(identity=username)

            tokenJWT = {
                'access_token': f'{access_token}'
            }

            return jsonify(tokenJWT), 200

    return jsonify({'msg': 'Credenciais inválidas!'}), 401