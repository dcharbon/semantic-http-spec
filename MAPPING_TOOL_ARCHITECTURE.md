# Semantic HTTP Mapping Tool Architecture

## Overview

The Semantic HTTP Mapping Tool is a suite of utilities that enables developers to create semantic wrappers around existing REST APIs without modifying the original APIs. The tool provides three primary components:

1. **Mapping Assistant** - AI-powered tool to help create mappings
2. **Proxy Generator** - Generates deployable proxy services from mappings
3. **Validation Tool** - Tests and validates mappings against live APIs

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Mapping Assistant                         │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  OpenAPI   │→ │   Semantic   │→ │   Mapping YAML   │   │
│  │  Analyzer  │  │   Inference  │  │    Generator     │   │
│  └────────────┘  └──────────────┘  └──────────────────┘   │
│         ↓               ↓                    ↓              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Interactive Refinement UI                   │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↓
                   Mapping Specification
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Proxy Generator                           │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  Mapping   │→ │   Code Gen   │→ │  Deployable      │   │
│  │  Parser    │  │   Templates  │  │  Proxy Service   │   │
│  └────────────┘  └──────────────┘  └──────────────────┘   │
│                                                              │
│  Supports: Python/Flask, Node/Express, Go, Rust             │
└─────────────────────────────────────────────────────────────┘
                            ↓
                   Proxy Service (Running)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   Validation Tool                            │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  Test      │→ │   Execute    │→ │  Validation      │   │
│  │  Generator │  │   Tests      │  │  Report          │   │
│  └────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component 1: Mapping Assistant

### Purpose
Help developers create accurate mapping specifications with minimal manual effort.

### Key Features

#### 1. OpenAPI Analyzer
- Parses existing OpenAPI specifications
- Extracts endpoints, methods, schemas
- Identifies data types and relationships

#### 2. Semantic Inference Engine
- Analyzes field names to suggest schema.org mappings
- Uses AI/LLM to identify semantic types
- Suggests RDF properties based on context
- Leverages common vocabularies (schema.org, FOAF, Dublin Core)

#### 3. Interactive Refinement UI
- CLI or web-based interface
- Shows suggested mappings
- Allows developers to accept/modify/reject suggestions
- Provides context-sensitive help

### Minimal Viable Implementation

```python
# Command-line interface
$ semantic-map init stripe-customers.yaml \
    --openapi https://stripe.com/openapi/spec.yaml \
    --endpoint /v1/customers/{id} \
    --semantic-base https://semantic.stripe.com

# Analyzes endpoint and suggests mappings
Analyzing Stripe API endpoint /v1/customers/{id}...

Found fields:
  ✓ id (string) → Suggested: schema:identifier
  ✓ email (string, format: email) → Suggested: schema:email
  ✓ name (string) → Suggested: schema:name
  ? description (string) → Suggested: schema:description
  ? metadata (object) → Suggested: stripe:metadata (custom)

Suggested resource type: schema:Person

Accept all suggestions? [Y/n/review]
> review

# Interactive review mode
[1/5] Field: email
  Source: $.email
  Semantic: email
  Property: schema:email
  Type: string

Accept? [Y/n/edit/skip]
> y

# ... continues for each field

# Generates mapping YAML
✓ Generated mapping: stripe-customers-mapping.yaml
✓ Generated context: stripe-customers-context.jsonld
✓ Generated schema: stripe-customers-schema.json

Next steps:
  1. Review generated files
  2. Test mapping: semantic-map validate stripe-customers-mapping.yaml
  3. Generate proxy: semantic-map generate stripe-customers-mapping.yaml
```

### Architecture

```python
class MappingAssistant:
    def __init__(self, openapi_spec: str):
        self.openapi = OpenAPIParser(openapi_spec)
        self.semantic_engine = SemanticInferenceEngine()

    def analyze_endpoint(self, path: str) -> EndpointAnalysis:
        """Analyze an endpoint and suggest semantic mappings"""
        schema = self.openapi.get_schema_for_path(path)
        suggestions = self.semantic_engine.infer_semantics(schema)
        return EndpointAnalysis(schema, suggestions)

    def generate_mapping(self, analysis: EndpointAnalysis,
                        user_refinements: dict) -> MappingSpec:
        """Generate final mapping specification"""
        mapping = MappingSpec()
        # Apply user refinements to suggestions
        # Generate context and schema files
        return mapping

class SemanticInferenceEngine:
    def __init__(self):
        self.vocabulary = load_vocabularies(['schema.org', 'foaf'])
        self.llm = LanguageModel()  # For complex inference

    def infer_semantics(self, schema: dict) -> Suggestions:
        """Infer semantic types from schema"""
        suggestions = []

        # Rule-based inference
        for field, definition in schema['properties'].items():
            if field == 'email' and definition.get('format') == 'email':
                suggestions.append({
                    'field': field,
                    'property': 'schema:email',
                    'confidence': 0.95
                })
            # ... more rules

        # LLM-based inference for complex cases
        complex_fields = identify_complex_fields(schema)
        llm_suggestions = self.llm.suggest_semantics(complex_fields)
        suggestions.extend(llm_suggestions)

        return Suggestions(suggestions)
```

## Component 2: Proxy Generator

### Purpose
Generate deployable proxy services from mapping specifications.

### Key Features

1. **Multi-language Support** - Generate Python, Node.js, Go, or Rust proxies
2. **Standards Compliance** - Generated proxies fully implement Semantic HTTP spec
3. **Performance Optimization** - Includes caching, connection pooling
4. **Observability** - Built-in logging, metrics, tracing

### Minimal Viable Implementation

```python
# Generate proxy service
$ semantic-map generate stripe-customers-mapping.yaml \
    --language python \
    --output ./stripe-semantic-proxy

Generating Python/Flask proxy service...
  ✓ Generated proxy server: stripe-semantic-proxy/app.py
  ✓ Generated Docker configuration
  ✓ Generated requirements.txt
  ✓ Generated README with deployment instructions

Run your proxy:
  $ cd stripe-semantic-proxy
  $ pip install -r requirements.txt
  $ python app.py

Your semantic API will be available at:
  http://localhost:8080/customers/{id}

Test with:
  $ curl -X OPTIONS http://localhost:8080/customers/cus_test123
```

### Generated Proxy Structure

```
stripe-semantic-proxy/
├── app.py                    # Main application
├── mapping.yaml             # Copy of mapping spec
├── requirements.txt         # Dependencies
├── Dockerfile              # Container image
├── docker-compose.yml      # Easy deployment
├── README.md              # Usage instructions
├── handlers/
│   ├── __init__.py
│   ├── customers.py       # Customer endpoint handlers
│   └── transformations.py # Field transformations
├── schemas/
│   ├── customer-schema.json
│   └── customer-context.jsonld
└── tests/
    └── test_customers.py  # Generated tests
```

### Core Proxy Implementation

```python
# Generated app.py (simplified)
from flask import Flask, request, jsonify, Response
import requests
from handlers.customers import CustomerHandler
from handlers.transformations import apply_transformations

app = Flask(__name__)
mapping = load_mapping('mapping.yaml')
customer_handler = CustomerHandler(mapping)

@app.route('/customers/<customer_id>', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
def customer_endpoint(customer_id):
    if request.method == 'OPTIONS':
        return customer_handler.handle_options(customer_id)
    elif request.method == 'GET':
        return customer_handler.handle_get(customer_id)
    elif request.method == 'PUT':
        return customer_handler.handle_put(customer_id, request.json)
    elif request.method == 'DELETE':
        return customer_handler.handle_delete(customer_id)

# handlers/customers.py
class CustomerHandler:
    def __init__(self, mapping):
        self.mapping = mapping
        self.source_api = SourceAPIClient(mapping.metadata.baseUrl)

    def handle_options(self, customer_id):
        """Return HTTP Schema Resource"""
        options_schema = {
            "get": {
                "responses": {
                    "200": {
                        "description": "OK",
                        "content": {
                            "application/json": {
                                "schema": self.mapping.endpoints[0].schema.url,
                                "context": self.mapping.endpoints[0].context.url
                            }
                        }
                    }
                }
            },
            # ... other methods
        }

        headers = {
            'Link': f'<{self.mapping.endpoints[0].schema.url}>; rel="describedby"',
            'Link': f'<{self.mapping.endpoints[0].context.url}>; rel="http://www.w3.org/ns/json-ld#context"'
        }

        return jsonify(options_schema), 200, headers

    def handle_get(self, customer_id):
        """Retrieve customer from source API and transform"""
        # Call source API
        source_path = self.mapping.endpoints[0].source.path.format(id=customer_id)
        response = self.source_api.get(source_path,
                                      headers=self._forward_auth())

        if response.status_code != 200:
            return self._transform_error(response)

        # Transform response using mapping
        source_data = response.json()
        semantic_data = self._transform_response(source_data)

        # Add semantic headers
        headers = self._semantic_headers()

        return jsonify(semantic_data), 200, headers

    def _transform_response(self, source_data):
        """Transform source API response to semantic format"""
        semantic_data = {}
        response_mapping = self.mapping.endpoints[0].methods.get.responseMapping

        for field_map in response_mapping.fields:
            # Extract from source using JSONPath
            value = jsonpath(source_data, field_map.source)

            # Apply transformation if specified
            if field_map.transform:
                value = apply_transformation(field_map.transform, value)

            # Set in semantic response
            semantic_data[field_map.semantic] = value

        return semantic_data

    def _semantic_headers(self):
        """Generate standard semantic HTTP headers"""
        return {
            'Link': f'<{self.mapping.endpoints[0].schema.url}>; rel="describedby"',
            'Link': f'<{self.mapping.endpoints[0].context.url}>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
        }
```

## Component 3: Validation Tool

### Purpose
Test and validate mappings against live APIs to ensure correctness.

### Key Features

1. **Schema Validation** - Verify responses match JSON schemas
2. **Semantic Validation** - Check JSON-LD contexts are valid
3. **Integration Testing** - Test against live or mock APIs
4. **Regression Testing** - Detect API changes that break mappings

### Minimal Viable Implementation

```bash
# Validate a mapping
$ semantic-map validate stripe-customers-mapping.yaml \
    --api-key sk_test_... \
    --test-customer cus_test123

Running validation tests...

✓ Schema files are valid JSON Schema
✓ Context files are valid JSON-LD
✓ Mapping structure is valid

Testing against live API:
  ✓ GET /customers/cus_test123
    - Response matches schema
    - Semantic headers present
    - Field transformations correct

  ✓ OPTIONS /customers/cus_test123
    - Returns HTTP Schema Resource
    - Schema and context URLs correct

  ✓ PUT /customers/cus_test123
    - Request transformation correct
    - Response matches schema

All tests passed! Mapping is valid.
```

### Architecture

```python
class MappingValidator:
    def __init__(self, mapping_file: str):
        self.mapping = load_mapping(mapping_file)
        self.validator = SchemaValidator()

    def validate_structure(self) -> ValidationReport:
        """Validate mapping file structure"""
        # Check YAML is valid
        # Check all required fields present
        # Validate references
        pass

    def validate_schemas(self) -> ValidationReport:
        """Validate JSON schemas and contexts"""
        # Load and validate JSON Schema files
        # Load and validate JSON-LD contexts
        # Check for broken references
        pass

    def validate_against_api(self, credentials: dict) -> ValidationReport:
        """Test mapping against live API"""
        results = []

        for test_case in self.mapping.validation.testCases:
            result = self._execute_test_case(test_case, credentials)
            results.append(result)

        return ValidationReport(results)

    def _execute_test_case(self, test: TestCase, credentials: dict):
        """Execute a single test case"""
        # Make request to proxy
        # Verify response status
        # Validate response against schema
        # Check semantic headers
        # Validate transformations
        pass
```

## Deployment Models

### 1. Local Development Proxy
Run proxy locally during development:
```bash
$ semantic-map run stripe-customers-mapping.yaml --port 8080
Semantic HTTP Proxy running at http://localhost:8080
```

### 2. Containerized Deployment
Deploy as Docker container:
```bash
$ semantic-map generate stripe-customers-mapping.yaml --docker
$ cd output && docker-compose up
```

### 3. Serverless Deployment
Deploy to AWS Lambda, Google Cloud Functions, etc.:
```bash
$ semantic-map deploy stripe-customers-mapping.yaml \
    --platform aws-lambda \
    --region us-east-1
```

### 4. Edge Deployment
Deploy to Cloudflare Workers, Fastly Compute@Edge:
```bash
$ semantic-map deploy stripe-customers-mapping.yaml \
    --platform cloudflare-workers
```

### 5. Client-Side Only
Generate client library without proxy:
```bash
$ semantic-map generate-client stripe-customers-mapping.yaml \
    --language typescript \
    --output ./stripe-semantic-client

# Uses mapping for type generation and semantic understanding
# Makes requests directly to source API
# No proxy needed
```

## Implementation Phases

### Phase 1: Core Mapping Assistant (MVP)
- [ ] Mapping file parser/validator
- [ ] Basic semantic inference (rule-based)
- [ ] CLI for creating mappings
- [ ] Schema and context generation

### Phase 2: Proxy Generator
- [ ] Python/Flask proxy generator
- [ ] Response transformation engine
- [ ] OPTIONS method implementation
- [ ] Basic caching

### Phase 3: Validation Tool
- [ ] Schema validation
- [ ] Integration test runner
- [ ] Validation reporting

### Phase 4: Advanced Features
- [ ] LLM-powered semantic inference
- [ ] Multi-language proxy generation
- [ ] Community mapping registry
- [ ] Visual mapping editor

## Technology Stack

### Core Tools
- **Language**: Python 3.10+
- **CLI Framework**: Click or Typer
- **YAML Parser**: PyYAML
- **JSON Schema**: jsonschema
- **JSON-LD**: PyLD
- **OpenAPI**: openapi-spec-validator

### Proxy Generation
- **Python**: Flask/FastAPI
- **Node.js**: Express/Fastify
- **Go**: Chi/Gin
- **Rust**: Actix/Axum

### AI/ML
- **Semantic Inference**: OpenAI API, Anthropic Claude, or local LLMs
- **Vector DB**: For semantic similarity (optional)

### Testing
- **Unit Tests**: pytest
- **Integration Tests**: pytest + requests
- **Validation**: JSON Schema validators

## Next Steps

1. **Prototype the Mapping Assistant** - Core CLI tool
2. **Create Reference Mappings** - 2-3 popular APIs
3. **Build Simple Proxy Generator** - Python only initially
4. **Establish Community** - GitHub repo, Discord, documentation
5. **Seek Feedback** - From API providers and consumers

---

Copyright © 2025 David Charboneau
