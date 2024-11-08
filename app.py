# Bibliotecas
from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import secrets

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32)
app.config['JWT_ALGORITHM'] = 'HS512'
jwt = JWTManager(app)

swagger = Swagger(app,
                  template={
                      "info": {
                          "title": "API do Star Wars",
                          "description": "Documentação da API que fornece dados sobre o universo de Star Wars",
                          "version": "1.0.0",
                          "contact": {
                              "name": "Marcelo Augusto de Mello Paixão",
                              "email": "marceloamellopaixao@gmail.com",  # Adicione o domínio do e-mail
                              "url": "https://github.com/marceloamellopaixao/API_StarWars_Desafio_PowerOfData"
                          },
                      },
                      "securityDefinitions": {
                          "JWT": {
                              "type": "apiKey",
                              "name": "Authorization",
                              "in": "header",
                              "description": "Token JWT gerado após o login. \n\nInsira da seguinte forma: (Bearer $token)"
                          }
                      },
                      "security": [
                          {"JWT": []}
                      ]
                  })

@app.route('/')
def home_app():
    """Home page da API
    ---
    tags:
      - Início
    responses:
      200:
        description: Página inicial da API. Veja uma prévia [aqui](/)
      400:
        description: Página inicial não encontrada!
    """
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)