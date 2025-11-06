#!/usr/bin/env python3
"""
Semantic HTTP Mapper - Proof of Concept

A minimal viable tool for creating and managing semantic HTTP mappings.
This POC demonstrates the core concepts of the mapping tool architecture.

Copyright © 2025 David Charboneau
"""

import yaml
import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class FieldMapping:
    """Represents a field mapping from source to semantic format"""
    source: str  # JSONPath expression
    semantic: str  # Semantic field name
    semantic_property: str  # RDF property URI
    type: str  # JSON Schema type
    transform: Optional[str] = None
    required: bool = False
    description: str = ""


@dataclass
class SemanticSuggestion:
    """A suggested semantic mapping"""
    field_name: str
    semantic_property: str
    rdf_type: Optional[str]
    confidence: float
    reason: str


class SemanticInferenceEngine:
    """
    Infers semantic types from API schemas.
    Uses rule-based approach for POC; can be extended with LLM.
    """

    # Common field name patterns and their schema.org mappings
    FIELD_PATTERNS = {
        r'^(email|email_address|e_mail)$': ('schema:email', 0.95),
        r'^(name|full_name|fullname)$': ('schema:name', 0.9),
        r'^(first_name|firstname|given_name)$': ('schema:givenName', 0.9),
        r'^(last_name|lastname|family_name|surname)$': ('schema:familyName', 0.9),
        r'^(phone|telephone|phone_number)$': ('schema:telephone', 0.9),
        r'^(address)$': ('schema:address', 0.85),
        r'^(street|street_address)$': ('schema:streetAddress', 0.85),
        r'^(city)$': ('schema:addressLocality', 0.85),
        r'^(state|region|province)$': ('schema:addressRegion', 0.85),
        r'^(zip|postal_code|zipcode|postcode)$': ('schema:postalCode', 0.9),
        r'^(country)$': ('schema:addressCountry', 0.9),
        r'^(description|desc)$': ('schema:description', 0.8),
        r'^(id|identifier)$': ('schema:identifier', 0.9),
        r'^(url|link)$': ('schema:url', 0.85),
        r'^(image|photo|picture)$': ('schema:image', 0.85),
        r'^(created_at|created|date_created)$': ('schema:dateCreated', 0.9),
        r'^(updated_at|modified|date_modified)$': ('schema:dateModified', 0.9),
        r'^(price|cost|amount)$': ('schema:price', 0.8),
        r'^(currency)$': ('schema:priceCurrency', 0.9),
    }

    # Type hints from JSON Schema
    TYPE_HINTS = {
        'email': 'schema:email',
        'date-time': 'schema:DateTime',
        'date': 'schema:Date',
        'uri': 'schema:URL',
    }

    def infer_field_mapping(self, field_name: str, field_schema: Dict[str, Any]) -> SemanticSuggestion:
        """Infer semantic mapping for a single field"""

        # Normalize field name
        normalized = field_name.lower()

        # Check format hints
        if 'format' in field_schema:
            format_type = field_schema['format']
            if format_type in self.TYPE_HINTS:
                return SemanticSuggestion(
                    field_name=field_name,
                    semantic_property=self.TYPE_HINTS[format_type],
                    rdf_type=None,
                    confidence=0.95,
                    reason=f"Detected from JSON Schema format: {format_type}"
                )

        # Pattern matching
        for pattern, (property_uri, confidence) in self.FIELD_PATTERNS.items():
            if re.match(pattern, normalized, re.IGNORECASE):
                return SemanticSuggestion(
                    field_name=field_name,
                    semantic_property=property_uri,
                    rdf_type=None,
                    confidence=confidence,
                    reason=f"Matched pattern: {pattern}"
                )

        # Default: use field name as-is with custom namespace
        return SemanticSuggestion(
            field_name=field_name,
            semantic_property=f"api:{field_name}",
            rdf_type=None,
            confidence=0.5,
            reason="No pattern match found, using custom namespace"
        )

    def infer_resource_type(self, schema: Dict[str, Any]) -> Optional[str]:
        """Infer the RDF type for a resource based on its schema"""

        if 'properties' not in schema:
            return None

        properties = schema['properties'].keys()

        # Check for person indicators
        person_indicators = {'email', 'name', 'first_name', 'last_name', 'phone'}
        if len(person_indicators.intersection(properties)) >= 2:
            return 'schema:Person'

        # Check for organization indicators
        org_indicators = {'company', 'organization', 'company_name'}
        if len(org_indicators.intersection(properties)) >= 1:
            return 'schema:Organization'

        # Check for product indicators
        product_indicators = {'price', 'sku', 'product_name'}
        if len(product_indicators.intersection(properties)) >= 2:
            return 'schema:Product'

        return None


class MappingGenerator:
    """Generates mapping specifications from OpenAPI schemas"""

    def __init__(self):
        self.inference_engine = SemanticInferenceEngine()

    def generate_mapping(
        self,
        api_name: str,
        api_version: str,
        base_url: str,
        endpoint_path: str,
        endpoint_schema: Dict[str, Any],
        semantic_base_url: str
    ) -> Dict[str, Any]:
        """Generate a mapping specification for an endpoint"""

        # Infer resource type
        resource_type = self.inference_engine.infer_resource_type(endpoint_schema)

        # Generate field mappings
        field_mappings = []
        if 'properties' in endpoint_schema:
            for field_name, field_schema in endpoint_schema['properties'].items():
                suggestion = self.inference_engine.infer_field_mapping(
                    field_name, field_schema
                )

                mapping = FieldMapping(
                    source=f"$.{field_name}",
                    semantic=field_name,  # Keep same name for simplicity
                    semantic_property=suggestion.semantic_property,
                    type=field_schema.get('type', 'string'),
                    required=field_name in endpoint_schema.get('required', []),
                    description=field_schema.get('description', '')
                )
                field_mappings.append(asdict(mapping))

        # Generate mapping structure
        mapping = {
            '$schema': 'https://semantic-http-spec.org/mapping-schema/v0.1',
            'version': '0.1',
            'metadata': {
                'apiName': api_name,
                'apiVersion': api_version,
                'mappingVersion': '1.0.0',
                'baseUrl': base_url,
                'semanticBaseUrl': semantic_base_url,
            },
            'semanticContext': {
                'contextUrl': f'{semantic_base_url}/context.jsonld',
                'vocabularies': [
                    {'namespace': 'schema', 'uri': 'http://schema.org/'}
                ]
            },
            'endpoints': [
                {
                    'path': endpoint_path,
                    'source': {
                        'path': endpoint_path
                    },
                    'semanticType': resource_type or 'schema:Thing',
                    'schema': {
                        'url': f'{semantic_base_url}/schema.json',
                        'deriveFrom': 'transform'
                    },
                    'context': {
                        'url': f'{semantic_base_url}/context.jsonld'
                    },
                    'methods': {
                        'get': {
                            'enabled': True,
                            'responseMapping': {
                                'fields': field_mappings
                            },
                            'responses': {
                                '200': {
                                    'description': 'Success',
                                    'schema': f'{semantic_base_url}/schema.json',
                                    'context': f'{semantic_base_url}/context.jsonld'
                                }
                            }
                        }
                    }
                }
            ]
        }

        return mapping

    def generate_context(self, field_mappings: List[FieldMapping]) -> Dict[str, Any]:
        """Generate JSON-LD context from field mappings"""

        context = {
            '@context': {
                '@version': 1.1,
                'schema': 'http://schema.org/',
                'xsd': 'http://www.w3.org/2001/XMLSchema#',
            }
        }

        # Add field mappings to context
        for mapping in field_mappings:
            context['@context'][mapping.semantic] = {
                '@id': mapping.semantic_property,
                '@type': self._json_to_xsd_type(mapping.type)
            }

        return context

    def generate_schema(
        self,
        field_mappings: List[FieldMapping],
        resource_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate JSON Schema from field mappings"""

        properties = {}
        required = []

        for mapping in field_mappings:
            properties[mapping.semantic] = {
                'type': mapping.type,
                'description': mapping.description,
                'x-semantic-property': mapping.semantic_property
            }
            if mapping.required:
                required.append(mapping.semantic)

        schema = {
            '$schema': 'http://json-schema.org/draft-07/schema#',
            'type': 'object',
            'properties': properties,
            'required': required
        }

        if resource_type:
            schema['x-semantic-type'] = resource_type

        return schema

    def _json_to_xsd_type(self, json_type: str) -> str:
        """Map JSON Schema type to XSD type"""
        type_map = {
            'string': 'xsd:string',
            'number': 'xsd:decimal',
            'integer': 'xsd:integer',
            'boolean': 'xsd:boolean',
            'object': '@id',
            'array': '@list'
        }
        return type_map.get(json_type, 'xsd:string')


class ProxyGenerator:
    """Generates deployable proxy code from mapping specifications"""

    def generate_flask_proxy(self, mapping: Dict[str, Any], output_dir: Path):
        """Generate a Flask proxy service"""

        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate main app.py
        app_code = self._generate_flask_app(mapping)
        (output_dir / 'app.py').write_text(app_code)

        # Generate requirements.txt
        requirements = [
            'flask>=2.3.0',
            'requests>=2.31.0',
            'jsonpath-ng>=1.6.0',
            'PyYAML>=6.0',
        ]
        (output_dir / 'requirements.txt').write_text('\n'.join(requirements))

        # Copy mapping
        (output_dir / 'mapping.yaml').write_text(yaml.dump(mapping))

        # Generate README
        readme = self._generate_readme(mapping)
        (output_dir / 'README.md').write_text(readme)

        print(f"✓ Generated Flask proxy in {output_dir}")
        print(f"\nTo run:")
        print(f"  cd {output_dir}")
        print(f"  pip install -r requirements.txt")
        print(f"  python app.py")

    def _generate_flask_app(self, mapping: Dict[str, Any]) -> str:
        """Generate Flask application code"""

        return f'''#!/usr/bin/env python3
"""
Semantic HTTP Proxy
Auto-generated from mapping specification
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
    result = {{}}

    for field in field_mappings:
        # Extract value using JSONPath
        jsonpath_expr = parse(field['source'])
        matches = [match.value for match in jsonpath_expr.find(source_data)]

        if matches:
            result[field['semantic']] = matches[0]

    return result

def semantic_headers(endpoint_config):
    """Generate semantic HTTP headers"""
    return {{
        'Link': f"<{{endpoint_config['schema']['url']}}>; rel=\\"describedby\\"",
        'Link': f"<{{endpoint_config['context']['url']}}>; rel=\\"http://www.w3.org/ns/json-ld#context\\"",
    }}

@app.route('{mapping['endpoints'][0]['path']}', methods=['GET', 'OPTIONS'])
def handle_endpoint():
    endpoint_config = mapping['endpoints'][0]

    if request.method == 'OPTIONS':
        # Return HTTP Schema Resource
        options_response = {{
            'get': {{
                'responses': {{
                    '200': {{
                        'description': 'OK',
                        'content': {{
                            'application/json': {{
                                'schema': endpoint_config['schema']['url'],
                                'context': endpoint_config['context']['url']
                            }}
                        }}
                    }}
                }}
            }}
        }}

        return jsonify(options_response), 200, semantic_headers(endpoint_config)

    # GET request - proxy to source API
    source_path = endpoint_config['source']['path']

    # Forward authentication if present
    auth_headers = {{}}
    if 'Authorization' in request.headers:
        auth_headers['Authorization'] = request.headers['Authorization']

    # Call source API
    response = requests.get(
        f"{{SOURCE_API}}{{source_path}}",
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
'''

    def _generate_readme(self, mapping: Dict[str, Any]) -> str:
        """Generate README for proxy service"""

        api_name = mapping['metadata']['apiName']
        base_url = mapping['metadata']['semanticBaseUrl']

        return f'''# Semantic HTTP Proxy for {api_name}

Auto-generated proxy service that implements the Semantic HTTP Resource specification.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python app.py
```

The proxy will be available at: http://localhost:8080

## Usage

### Discover capabilities
```bash
curl -X OPTIONS http://localhost:8080{mapping['endpoints'][0]['path']}
```

### Get resource
```bash
curl http://localhost:8080{mapping['endpoints'][0]['path']}
```

## Semantic Features

This proxy adds the following semantic features:

- **Schema Link Header**: Points to JSON Schema describing the resource
- **Context Link Header**: Points to JSON-LD context for semantic interpretation
- **OPTIONS Support**: Returns HTTP Schema Resource describing all operations

## Source API

- Base URL: {mapping['metadata']['baseUrl']}
- Version: {mapping['metadata']['apiVersion']}

## Semantic API

- Base URL: {base_url}
'''


def main():
    """Example usage"""

    # Example: Generate mapping for a simple user API
    example_schema = {
        'type': 'object',
        'required': ['id', 'email'],
        'properties': {
            'id': {'type': 'string', 'description': 'User ID'},
            'email': {'type': 'string', 'format': 'email', 'description': 'Email address'},
            'name': {'type': 'string', 'description': 'Full name'},
            'phone': {'type': 'string', 'description': 'Phone number'},
            'created_at': {'type': 'string', 'format': 'date-time', 'description': 'Creation date'},
        }
    }

    generator = MappingGenerator()

    # Generate mapping
    mapping = generator.generate_mapping(
        api_name='Example User API',
        api_version='v1',
        base_url='https://api.example.com',
        endpoint_path='/users/{id}',
        endpoint_schema=example_schema,
        semantic_base_url='https://semantic.example.com'
    )

    # Save mapping
    output_file = Path('example-mapping.yaml')
    with open(output_file, 'w') as f:
        yaml.dump(mapping, f, default_flow_style=False, sort_keys=False)

    print(f"✓ Generated mapping: {output_file}")

    # Generate context
    field_mappings = [
        FieldMapping(**field) for field in
        mapping['endpoints'][0]['methods']['get']['responseMapping']['fields']
    ]
    context = generator.generate_context(field_mappings)

    context_file = Path('example-context.jsonld')
    with open(context_file, 'w') as f:
        json.dump(context, f, indent=2)

    print(f"✓ Generated context: {context_file}")

    # Generate schema
    schema = generator.generate_schema(
        field_mappings,
        resource_type=mapping['endpoints'][0]['semanticType']
    )

    schema_file = Path('example-schema.json')
    with open(schema_file, 'w') as f:
        json.dump(schema, f, indent=2)

    print(f"✓ Generated schema: {schema_file}")

    # Generate proxy
    proxy_generator = ProxyGenerator()
    proxy_generator.generate_flask_proxy(mapping, Path('example-proxy'))


if __name__ == '__main__':
    main()
