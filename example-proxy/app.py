#!/usr/bin/env python3
"""
Semantic HTTP Proxy
Auto-generated from mapping specification

Copyright © 2025 David Charboneau
"""

from flask import Flask, request, jsonify
import requests
import yaml
from jsonpath_ng import parse

app = Flask(__name__)

# Load mapping
with open('mapping.yaml', 'r') as f:
    mapping = yaml.safe_load(f)

SOURCE_API = mapping['metadata']['baseUrl']

def transform_response(source_data, field_mappings):
    """Transform source API response to semantic format"""
    result = {}

    for field in field_mappings:
        # Extract value using JSONPath
        jsonpath_expr = parse(field['source'])
        matches = [match.value for match in jsonpath_expr.find(source_data)]

        if matches:
            result[field['semantic']] = matches[0]

    return result

def semantic_headers(endpoint_config):
    """Generate semantic HTTP headers"""
    return {
        'Link': f"<{endpoint_config['schema']['url']}>; rel=\"describedby\"",
        'Link': f"<{endpoint_config['context']['url']}>; rel=\"http://www.w3.org/ns/json-ld#context\"",
    }

@app.route('/users/{id}', methods=['GET', 'OPTIONS'])
def handle_endpoint():
    endpoint_config = mapping['endpoints'][0]

    if request.method == 'OPTIONS':
        # Return HTTP Schema Resource
        options_response = {
            'get': {
                'responses': {
                    '200': {
                        'description': 'OK',
                        'content': {
                            'application/json': {
                                'schema': endpoint_config['schema']['url'],
                                'context': endpoint_config['context']['url']
                            }
                        }
                    }
                }
            }
        }

        return jsonify(options_response), 200, semantic_headers(endpoint_config)

    # GET request - proxy to source API
    source_path = endpoint_config['source']['path']

    # Forward authentication if present
    auth_headers = {}
    if 'Authorization' in request.headers:
        auth_headers['Authorization'] = request.headers['Authorization']

    # Call source API
    response = requests.get(
        f"{SOURCE_API}{source_path}",
        headers=auth_headers
    )

    if response.status_code != 200:
        return response.json(), response.status_code

    # Transform response
    source_data = response.json()
    field_mappings = endpoint_config['methods']['get']['responseMapping']['fields']
    semantic_data = transform_response(source_data, field_mappings)

    return jsonify(semantic_data), 200, semantic_headers(endpoint_config)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
