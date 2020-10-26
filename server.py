from flask import Flask
# import the configs
from config import Server
# import the blueprints
from app_blueprint import app_blueprint
from backend_blueprint import backend_blueprint
# import the rate limiter
from security.rate_limiter import rate_limit


server = Flask(__name__)
server.secret_key = Server.session_secret

# register the visit rate limiter  
server.before_request(rate_limit)

if __name__ == '__main__':
    # register all blueprints here
    server.register_blueprint(app_blueprint)
    server.register_blueprint(backend_blueprint)
    # end of registeration
    server.run(
        host = Server.host,
        port = Server.port,
        debug = Server.debug
    )


