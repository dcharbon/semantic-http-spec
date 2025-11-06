# Semantic HTTP Proxy for Example User API

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
curl -X OPTIONS http://localhost:8080/users/{id}
```

### Get resource
```bash
curl http://localhost:8080/users/{id}
```

## Semantic Features

This proxy adds the following semantic features:

- **Schema Link Header**: Points to JSON Schema describing the resource
- **Context Link Header**: Points to JSON-LD context for semantic interpretation
- **OPTIONS Support**: Returns HTTP Schema Resource describing all operations

## Source API

- Base URL: https://api.example.com
- Version: v1

## Semantic API

- Base URL: https://semantic.example.com
