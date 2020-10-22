from flask import Flask
from config import Server
from app_blueprint import app_blueprint
from backend_blueprint import backend_blueprint
from security.rate_limiter import rate_limit

server = Flask(__name__)
server.secret_key = Server.session_secret



    
server.before_request(rate_limit)

if __name__ == '__main__':
    # TODO: register all blueprints here
    
    server.register_blueprint(app_blueprint)
    server.register_blueprint(backend_blueprint)
    server.run(
        host = Server.host,
        port = Server.port,
        debug = Server.debug
    )
