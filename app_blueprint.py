import base64
import datetime
from flask import Blueprint, render_template, request, jsonify, send_file, session
import config
from data.models import FinanceData
from data.data_interactive_layer import new_record


app_blueprint = Blueprint('App Blueprint', __name__)


@app_blueprint.route('/', methods = ['GET'])
def index():
    # gives the client app page
    return send_file('templates/index-vue.html')

@app_blueprint.route('/new-record', methods = ['POST'])
def _new_record():
    # as this is a trusted user, server-side validation is currently unimplemented.
    # TODO: server-side validation.
    admin_password = request.json.get('password')
    amount = int(float(request.json.get('amount')))
    tags = request.json.get('tags')
    describtion = request.json.get('description')
    
    # check whether the source has the permission
    if config.Server.admin_secret != admin_password and config.Server.api_key != admin_password:
        return '', 403
    
    # add the record: call the logic layer
    new_record(FinanceData(amount, datetime.datetime.now(), tags, describtion))
    
    return jsonify({'status': 0})
    
