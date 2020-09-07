from flask import Blueprint, render_template, request
import base64
from data.mock_data_interactive_layer import obtain_range

app_blueprint = Blueprint('App Blueprint', __name__)

def _parse_page_range_string(hex_string, default_range = (0,20)):
    try:
        _bytes = bytes.fromhex(hex_string)
        string_to_parse = str(base64.b64decode(_bytes), encoding='ASCII')
        start, end = string_to_parse.split('::')
        start = int(start)
        end = int(end)
        return start, end
    
    except Exception:
        # ignore non-parseble
        return default_range
    
def _form_page_range_string(start, end):
    return base64.b32encode(bytes('%s::%s'%(start, end))).hex()

@app_blueprint.route('/', methods = ['GET'])
def index():
    page_range = request.args.get('range', '')
    start, end = _parse_page_range_string(page_range)
    passed_object = {
        'start': start,
        'end': end,
        'finance_objects':  obtain_range(start, end) # mock
    }
    return render_template('index.html', data_object = passed_object)