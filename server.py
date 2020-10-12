from flask import Flask
from config import Server
from app_blueprint import app_blueprint
from backend_blueprint import backend_blueprint

server = Flask(__name__)
server.secret_key = Server.session_secret

if __name__ == '__main__':
    # TODO: register all blueprints here
    server.register_blueprint(app_blueprint)
    server.register_blueprint(backend_blueprint)
    server.run(
        host = Server.host,
        port = Server.port,
        debug = Server.debug
    )