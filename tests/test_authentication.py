import unittest
from flask import Flask
from flask_jwt_extended import JWTManager
import boto3
import json
from api.routes.auth import auth

class AuthTestCase(unittest.TestCase):
    """Classe de testes para verificar as funcionalidades de autenticação da API."""

    def setUp(self):
        """Configura a aplicação e o cliente de testes."""
        self.app = Flask(__name__)
        self.app.register_blueprint(auth)
        self.app.config['TESTING'] = True
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)
        self.client = self.app.test_client()

        # Configuração do S3 simulado
        self.s3 = boto3.client('s3', region_name='us-east-1')
        self.bucket_name = 'api-starwars-desafio-bucket'
        self.s3.create_bucket(Bucket=self.bucket_name)

        # Inicializa o arquivo JSON com um usuário para os testes
        initial_data = {"users": [{"username": "teste", "password": "teste123456"}]}
        self.s3.put_object(Bucket=self.bucket_name, Key='credentials/users-dev.json', Body=json.dumps(initial_data))

    def test_register_existing_user(self):
        """Testa o registro de um usuário já existente."""
        response = self.client.post('/register', json={
            'username': 'teste',  # Usuário já registrado na configuração do setUp
            'password': 'teste123456'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Usuário já existe!', response.get_json()['msg'])

    def test_register_empty_fields(self):
        """Testa o registro com campos vazios."""
        response = self.client.post('/register', json={
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Usuário ou Senha vazio!', response.get_json()['msg'])

    def test_login_success(self):
        """Testa o login bem-sucedido de um usuário existente."""
        response = self.client.post('/login', json={
            'username': 'teste',
            'password': 'teste123456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())

    def test_login_failure(self):
        """Testa o login com credenciais inválidas."""
        response = self.client.post('/login', json={
            'username': 'teste2',
            'password': 'teste123'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Credenciais inválidas!', response.get_json()['msg'])

if __name__ == '__main__':
    unittest.main()