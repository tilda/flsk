import flask
import json
import requests
from raven.contrib.flask import Sentry
secret_sentry = open('./secrets/sentry')
secret_udic = open('./secrets/urban')
sentry = Sentry(app, dsn=secret_sentry.read())
app = flask.Flask(__name__)

dad_headers = {
    'Accept': 'text/plain',
    'User-Agent': 'flsk (Flask API) - https://github.com/tilda/flsk'
}

uagent = {
    'User-Agent': 'flsk (Flask API) - https://github.com/tilda/flsk'
}

urban_headers = {
    'X-Mashape-Key': secret_udic.read(),
    'Accept': 'application/json'
}

@app.route("/api/joke")
def joke():
    jok = requests.get('https://icanhazdadjoke.com', headers=dad_headers)
    return jok.text

@app.route("/api/neko")
def neko():
    n = requests.get('https://nekos.life/api/neko', headers=uagent)
    return n.json()['neko']

@app.route("/api/urban/<word>")
def urban(word):
    u = requests.get('https://mashape-community-urban-dictionary.p.mashape.com/define?term={0}'.format(word), headers=urban_headers)
    if u.status == 200:
        d = u.json()
        d = d['list'][0]
        res = {
            'definition': d['definition'],
            'link': d['permalink']
        }
        return json.dumps(res)
    else:
        res = {'error': u.status}
        return json.dumps(res)
