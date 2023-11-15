from flask import Flask, Response, request, render_template
from model import database
import json

app = Flask(__name__)
db = database.Client()

@app.route('/', methods=['GET'])
def index():
    return Response(
        content_type='text/json', 
        response=json.dumps({
            'status': 'on'
        })
    )

@app.route('/data', methods=['GET'])
def data_index():
    return  render_template('httpcat.html', title="/data", image="https://http.cat/204")
    
@app.route('/data/<key>/<value>', methods=['GET'])
def select_where(key, value):
    key = key.lower()
    value = value.lower()
    
    if key not in db.keys:
        return Response(
            content_type='text/json', 
            response=json.dumps({
                'error': f'Invalid where {key}={value} clause. Make sure you are using one of the following: {db.keys} as your key.'
            }),
            status=400
        )
    
    response = db.query(key, value)

    return Response(
        content_type='text/json', 
        response=json.dumps({
            "success": True,
            'value': response,
        })
    )
    
@app.route('/data/<key>', methods=['GET'])
def select_unique(key):
    key = key.lower()
    
    if key not in db.keys:
        return Response(
            content_type='text/json', 
            response=json.dumps({
                'error': f'Invalid unique {key} clause. Make sure you are using one of the following: {db.keys} as your key.'
            }),
            status=400
        )
    
    response = db.unique(key)

    return Response(
        content_type='text/json', 
        response=json.dumps({
            "success": True,
            'value': response,
        })
    )
    
@app.route('/data/count/<key>/all', methods=['GET'])
def group_by_key(key):
    if key not in db.keys:
        return Response(
            content_type='text/json', 
            response=json.dumps({
                'error': f'Invalid key {key}. Make sure you are using one of the following: {db.keys} as your key.'
            }),
            status=400
        )
    
    columns = db.keys.copy()
    columns.remove('id')
    columns.remove(key)
    
    response = db.group_by(key, columns)
    
    return Response(
        content_type='text/json', 
        response=json.dumps({
            "success": True,
            'value': response,
        })
    )

if __name__ == '__main__':
    app.run(debug=True)