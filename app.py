# Bibliotecas
# import awsgi

from flask import Flask, render_template
from flask_jwt_extended import JWTManager
import secrets

# Functions Locals
from api.routes.auth import auth
from api.routes.films import films
from api.routes.people import people
from api.routes.planets import planets
from api.routes.starships import starships

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32)
app.config['JWT_ALGORITHM'] = 'HS512'
jwt = JWTManager(app)

@app.route('/')
def home_app():
    """
    Página Inicial da API
    """
    return render_template('base.html')
app.register_blueprint(auth)
app.register_blueprint(films)
app.register_blueprint(people)
app.register_blueprint(planets)
app.register_blueprint(starships)

# def lambda_handler(event, context):
#     return awsgi.response(app, event, context, base64_content_types={"image/png"})

if __name__ == '__main__':
    app.run(debug=True)