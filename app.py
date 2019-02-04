import os
from functools import wraps
from flask import Flask, redirect, url_for, request, render_template, jsonify, abort
from pymongo import MongoClient
from bson import json_util
from bson.json_util import dumps
import json
import uuid
from flask.logging import default_handler

app = Flask(__name__)

client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
db = client.datasets

uuid.uuid4().hex

if 'SECRET_KEY' in os.environ and os.environ['SECRET_KEY'] is not None:
   authtoken = os.environ['SECRET_KEY']
#   app.logger.debug("Auth token is " + str(authtoken))
else:
   #generate a unique auth token
   authtoken = uuid.uuid4().hex
#   app.logger.debug("Auth token is " + str(authtoken))
   app.logger.debug("Use this for posting content")
authtoken = "SECRET"
print("Auth token is " + str(authtoken))

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            print(request)
            if not 'Authorization' in request.headers:
               abort(401)

            user = None
            data = request.headers['Authorization'].encode('ascii','ignore')
            token = str.replace(str(data), 'Bearer ','')
            #try:
            #    user = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])['sub']
            #except:
            #    abort(401)
            if token != authtoken:
               abort(401)
            return f(user, *args, **kws)            
    return decorated_function

def isAuthorised(token):
   if token == authtoken:
      return True
   return False

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
    if not 'Authorization' in request.headers:
       abort(401)
    print(request.headers['Authorization'])
    data = request.headers['Authorization']
    token = str.replace(str(data), 'Bearer ', '')
    if token != authtoken: 
       return jsonify({ 'result' : 'not authorised' }),401
    content = request.json
    #db.datasets.insert_one(content, check_keys=False)
    db.datasets.insert(content, check_keys=False)

    return jsonify({ 'result' : 'success' }),200

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
