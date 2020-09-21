from flask import session, request, jsonify, Blueprint
from search_engine.filters import ComposedFilter
import os
from hashlib import sha256
from data.data_interactive_layer import obtain_all_data, obtain_stats

backend_blueprint = Blueprint('backend_blueprint', __name__)


def test_challenge(original, part):
    global challenges
    if not original in challenges:
        return False
    else:
        if sha256(bytes(original + part, encoding='ASCII')).hexdigest()[0:5].count('0') == 5:
            challenges.remove(original)
            return True
        return False
    
challenges = []

@backend_blueprint.route('/api/take-challenge')
def take_challenge():
    global challenges
    new_challenge = os.urandom(8).hex()
    challenges.append(new_challenge)
    return jsonify({
        'status': 0,
        'result': new_challenge
    })
    
@backend_blueprint.route('/api/stats', methods = ['GET'])
def stats():
    total_cost, total_revenue = obtain_stats()
    return jsonify({
        'total-revenue-cent': total_revenue,
        'total-cost-cent': total_cost
    })

@backend_blueprint.route('/api/poll/<challenge>/<nonce>', methods = ['GET'])
def poll_data(challenge, nonce):
    filtered_content = obtain_all_data()
    
    if session.get('serialized-filter', None) is not None:
        filtered_content = ComposedFilter.from_object(session['serialized-filter']).filter(filtered_content)
    
    global challenges
    if not challenge in challenges:
        return jsonify({
            'status': 1,
            'message': 'invalid challenge.'
        })
    elif not test_challenge(challenge, nonce):
        return jsonify({
            'status': 2,
            'message': 'test failure.'
        })
    
    return jsonify({
        'status': 0,
        'result': [_.to_object() for _ in filtered_content],
    })
    

