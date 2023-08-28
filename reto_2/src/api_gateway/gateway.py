from flask import Flask
from routes import file_services_bp
from api_gateway import LISTEN_IP, LISTEN_PORT

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'

app.register_blueprint(file_services_bp)

def run():
    app.run(host=LISTEN_IP,debug=True, port = LISTEN_PORT)
