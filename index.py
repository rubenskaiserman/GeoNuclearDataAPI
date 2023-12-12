from flask import Flask, Response, request, render_template
from model import database, util, analysis
import json

app = Flask(__name__)
db = database.Client()
analitics = analysis.Analysis()
helper = util.Client()

@app.route('/', methods=['GET'])
def index():
    return Response(
        content_type='text/json', 
        response=json.dumps({
            'status': 'on',
            'message': 'Welcome to the API. Please use the following endpoints: /data, /data/<key>, /data/<key>/<value>, /data/count/<key>/all'
        })
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('httpcat.html', title="404", image="https://http.cat/404"), 404

@app.route('/data', methods=['GET'])
def data_index():
    return  render_template('httpcat.html', title="/data", image="https://http.cat/204")

    
@app.route('/data/<key>/<value>', methods=['GET'])
def select_where(key, value):
    key = key.lower()
    value = value.lower()
    
    if db.data == []:
        db.start()
    
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
    
    if db.data == []:
        db.start()
    
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
    if db.data == []:
        db.start()
    
    
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

@app.route('/data/keys', methods=['GET'])
def keys():
    if db.data == []:
        db.start()
    keys = db.keys.copy()
    keys.remove('id')
    keys.remove('source')
    keys.remove('construction_start')
    keys.remove('operational_from')
    keys.remove('operational_to')
    keys.remove('capacity')
    
    return Response(
        content_type='text/json', 
        response=json.dumps({
            "success": True,
            'value': keys,
        })
    )

@app.route('/analysis', methods=['POST'])
def analysis():
    data = request.get_json()
    
    result = analitics.analyze(**data)
    
    
    return render_template('results.html', tables=result['tables'], graphs=result['graphs'])
    

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if db.data == []:
        db.start()
    keys = db.keys.copy()
    keys.remove('id')
    keys.remove('source')
    keys.remove('construction_start')
    keys.remove('operational_from')
    keys.remove('operational_to')
    keys.remove('capacity')
    
    columns = []
    for key in keys:
        columns.append([str(item) for item in db.unique(key)])
        
    titles = [key.replace("_", " ").title() for key in keys]
        
    return render_template('dashboard.html', columns=columns, titles=titles,keys=keys, keys_length=len(keys))

@app.route('/dashboard/download', methods=['POST'])
def download():
    data = request.get_json()
    print(data)
    
    return {'success': True}

if __name__ == '__main__':
    app.run(debug=False)