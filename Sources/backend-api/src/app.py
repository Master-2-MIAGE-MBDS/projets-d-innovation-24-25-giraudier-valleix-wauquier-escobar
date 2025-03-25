from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .routes.init import init_routes
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY'] = "secret_key" #os.getenv('SECRET_KEY') # Clé secrète pour sécuriser les sessions / signer les tokens 
    
    init_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)