from flask import Flask, Response, request
from model import database
import json

app = Flask(__name__)
db = database.Client()

class Key:
    keys = [
        'id',
        'name',
        'status',
        'country',
        'status',
        'reactor_type',
        'reactor_model',
        'construction_start',
        'operational_from',
        'operational_to',
        'capacity',
        'source',
    ]

@app.route('/', methods=['GET'])
def index():
    return Response(
        content_type='text/json', 
        response=json.dumps({
            'status': 'on'
        })
    )
    
@app.route('/data/<key>/<value>', methods=['GET'])
def query_data(key, value):
    key = key.lower()
    value = value.lower()
    
    if key not in Key.keys:
        return Response(
            content_type='text/json', 
            response=json.dumps({
                'error': f'Invalid where {key}={value} clause. Make sure you are using one of the following: {Key.keys} as your key.'
            }),
            status=400
        )
    
    # TODO: Search
    response = db.query(key, value)

    return Response(
        content_type='text/json', 
        response=json.dumps({
            "success": True,
            'value': response,
        })
    )
    

if __name__ == '__main__':
    app.run(debug=True)