import os
from flask import Flask, redirect, url_for, request, render_template, jsonify
from pymongo import MongoClient
from bson import json_util
from bson.json_util import dumps

import json


app = Flask(__name__)

client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
db = client.datasets

@app.route('/')
def list():
    _items = db.datasets.find()
    items = [item for item in _items]
    return render_template('index.html', items=items)

@app.route('/view')
def view():
    app.logger.debug(request.args)
    id = request.args.get('id')
    item = db.datasets.find_one( { 'id': id })
    item.pop('_id')
    jsonldStr = dumps(item,default=json_util.default, indent=4)
    app.logger.debug(jsonldStr)

    if request.args.get('format') is not None and request.args.get('format') == 'jsonld':
       return jsonify(item)

    return render_template('view.html', dataset=item, jsonld=jsonldStr)

@app.route('/new', methods=['POST'])
def new():
    app.logger.debug("JSON received...")
    app.logger.debug(request.json)
    content = request.json
    db.datasets.insert_one(content)

    return jsonify({ 'result' : 'success' })

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
