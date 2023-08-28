from flask import Flask
from routes import file_services_bp
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'

app.register_blueprint(file_services_bp)

load_dotenv()

PORT = os.getenv('PORT')

def run():
    app.run(host='0.0.0.0',debug=True, port = PORT)
