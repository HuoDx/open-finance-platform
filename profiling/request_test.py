import requests

from hashlib import sha256
import os
h = lambda s: sha256(bytes(s, encoding='ASCII')).hexdigest()


def test_challenge(original, part):
    coder = sha256()
    coder.update(bytes(original+part, encoding='ASCII'))
    if coder.hexdigest()[0:5].count('0') == 5:
        return True
    return False
    
def mine(challenge):
    nonce = os.urandom(8).hex()[:10]
    while not test_challenge(challenge,nonce):
        nonce = os.urandom(8).hex()[:10]
    return nonce

with requests.get('http://loopback.keeer.net:50085/api/take-challenge') as response:
    challenge = response.json().get('result')
    
print('mining...')
nonce = mine(challenge)
print('mined:', nonce, 'result', h(challenge+nonce))
import pprint
with requests.get('http://loopback.keeer.net:50085/api/poll/%s/%s'%(challenge, nonce)) as response:
    pprint.pprint(response.json())


