from flask import Blueprint, render_template, request, jsonify, send_file, session
import base64
import config
from data.models import FinanceData
from data.data_interactive_layer import new_record
import datetime

app_blueprint = Blueprint('App Blueprint', __name__)


@app_blueprint.route('/', methods = ['GET'])
def index():
    from data.models import FinanceData
    import datetime
    return send_file('templates/index-vue.html')

@app_blueprint.route('/new-record', methods = ['POST'])
def new_record():
    admin_password = request.form.get('password')
    amount = request.form.get('amount')
    tags = request.form.get('tags')
    describtion = request.form.get('description')
    if config.Server.admin_secret != admin_password:
        return '', 403
    new_record(FinanceData(amount, datetime.datetime.now(), tags, describtion))
    
