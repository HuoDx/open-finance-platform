from flask import Blueprint, render_template, request, jsonify, send_file, session
import base64
from data.mock_data_interactive_layer import obtain_range, obtain_total_number

app_blueprint = Blueprint('App Blueprint', __name__)


@app_blueprint.route('/', methods = ['GET'])
def index():
    from data.models import FinanceData
    import datetime
    return send_file('templates/index-vue.html')

