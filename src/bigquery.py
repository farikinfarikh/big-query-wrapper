from flask import Blueprint, request, jsonify
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from flasgger import swag_from

bq = Blueprint("bq",__name__,url_prefix="/api/")

@bq.post('query')
@swag_from('./docs/bigquery/bigquery.yaml')
def query():    
    if 'query' not in request.json:
        return jsonify({'error message': 'query is required'}), \
            HTTP_400_BAD_REQUEST
    query = request.json['query']
    client = bigquery.Client()
    try:
        results = client.query(query)
        df = results.to_dataframe()
        json_obj=df.to_json(orient='records')
    except BadRequest as e:
        error_message = []
        for e in results.errors:
            error_message.append('ERROR: {}'.format(e['message']))
        return jsonify(error_message), HTTP_400_BAD_REQUEST
            

    return json_obj, HTTP_201_CREATED