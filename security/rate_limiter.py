import time
from config import Server
from flask import request

ip_visits = {}

def rate_limit():
    if _get_token(request.remote_addr):
        return None
    return 'You are requesting too fast.', 403

def _get_token(request_ipv4: str) -> bool:
    global ip_visits
    if request_ipv4 not in ip_visits:
        ip_visits.update({request_ipv4: {
            'timestamp': time.time(),
            'tokens_in_bucket': int(Server.visits_per_second) + 1
        }})

    else:
        last_visit_timestamp = ip_visits.get(request_ipv4).get('timestamp')
        
        delta_tokens = int(float(time.time() - last_visit_timestamp) * Server.visits_per_second)
        new_tokens = ip_visits[request_ipv4]['tokens_in_bucket']
        new_tokens = Server.token_bucket_capacity if new_tokens + delta_tokens > Server.token_bucket_capacity else (new_tokens + delta_tokens)
        
        
        new_tokens -= 1
        ip_visits[request_ipv4]['tokens_in_bucket'] = new_tokens
        
        if new_tokens <= 0:
            return False
        
    return True
        
        