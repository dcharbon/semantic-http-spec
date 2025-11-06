# Semantic HTTP Mapping Guide

## Overview

This guide explains how to use the Semantic HTTP Mapping system to wrap existing REST APIs with semantic capabilities without modifying the original APIs.

## Table of Contents

1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [Mapping Specification Format](#mapping-specification-format)
4. [Using the Mapping Tool](#using-the-mapping-tool)
5. [Generating Proxies](#generating-proxies)
6. [Examples](#examples)
7. [Best Practices](#best-practices)
8. [FAQ](#faq)

## Introduction

### The Problem

REST APIs typically lack:
- **Self-description**: No standard way to discover schemas and capabilities
- **Semantic meaning**: Structure without understanding what data represents
- **Consistency**: Different APIs use different conventions for similar concepts

### The Solution

The Semantic HTTP Mapping system provides:
- **Wrapper specifications** that add semantic layers to existing APIs
- **Automated tools** to help create these wrappers
- **Proxy generators** to deploy semantic-compliant endpoints
- **Community sharing** of mappings for popular APIs

### Key Benefits

1. **Immediate adoption**: Works with any existing API
2. **AI-friendly**: Tools like Claude Code can understand and work with semantic APIs
3. **Cross-API integration**: Semantic understanding enables reasoning across different APIs
4. **Progressive enhancement**: Start simple, add richness over time

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/dcharbon/semantic-http-spec.git
cd semantic-http-spec

# Install dependencies (if needed)
pip install pyyaml jsonpath-ng flask requests
```

### Generate Your First Mapping

```bash
# Run the example
python tools/semantic_mapper.py

# This generates:
# - example-mapping.yaml (mapping specification)
# - example-context.jsonld (JSON-LD context)
# - example-schema.json (JSON Schema)
# - example-proxy/ (Flask proxy service)
```

### Test the Proxy

```bash
cd example-proxy
pip install -r requirements.txt
python app.py

# In another terminal:
curl -X OPTIONS http://localhost:8080/users/123
```

## Mapping Specification Format

### Basic Structure

```yaml
$schema: https://semantic-http-spec.org/mapping-schema/v0.1
version: "0.1"

metadata:
  apiName: "My API"
  apiVersion: "v1"
  baseUrl: "https://api.example.com"
  semanticBaseUrl: "https://semantic.example.com"

endpoints:
  - path: "/resources/{id}"
    source:
      path: "/v1/resources/{id}"

    methods:
      get:
        enabled: true
        responseMapping:
          fields:
            - source: "$.field_name"
              semantic: "fieldName"
              semantic_property: "schema:property"
              type: "string"
```

### Field Mappings

Field mappings transform source API fields to semantic fields:

```yaml
- source: "$.customer.email_address"  # JSONPath in source API
  semantic: "email"                    # Name in semantic API
  semantic_property: "schema:email"    # RDF property URI
  type: "string"                       # JSON Schema type
  transform: "lowercase"               # Optional transformation
  required: true                       # Whether field is required
  description: "Customer email"        # Human-readable description
```

### Transformations

Define reusable transformations:

```yaml
transformations:
  - name: "centsToDollars"
    description: "Convert cents to dollars"
    language: javascript
    code: |
      function transform(cents) {
        return cents / 100.0;
      }
    examples:
      - input: 1050
        output: 10.50
```

### Semantic Context

Define the JSON-LD context for semantic interpretation:

```yaml
semanticContext:
  contextUrl: "https://semantic.example.com/context.jsonld"
  vocabularies:
    - namespace: "schema"
      uri: "http://schema.org/"
  commonTypes:
    - name: "Customer"
      rdfType: "schema:Person"
```

## Using the Mapping Tool

### Programmatic Usage

```python
from tools.semantic_mapper import MappingGenerator

# Define your API schema
schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'},
        'email': {'type': 'string', 'format': 'email'},
        'name': {'type': 'string'},
    }
}

# Generate mapping
generator = MappingGenerator()
mapping = generator.generate_mapping(
    api_name='My API',
    api_version='v1',
    base_url='https://api.example.com',
    endpoint_path='/users/{id}',
    endpoint_schema=schema,
    semantic_base_url='https://semantic.example.com'
)

# Save mapping
import yaml
with open('my-mapping.yaml', 'w') as f:
    yaml.dump(mapping, f)
```

### Semantic Inference

The tool automatically infers semantic properties from field names:

| Field Name | Inferred Property | Confidence |
|------------|------------------|------------|
| `email`, `email_address` | `schema:email` | 95% |
| `name`, `full_name` | `schema:name` | 90% |
| `phone`, `telephone` | `schema:telephone` | 90% |
| `street`, `street_address` | `schema:streetAddress` | 85% |
| `city` | `schema:addressLocality` | 85% |
| `state`, `region` | `schema:addressRegion` | 85% |
| `zip`, `postal_code` | `schema:postalCode` | 90% |
| `created_at` | `schema:dateCreated` | 90% |

The tool also infers resource types:

| Fields Present | Inferred Type |
|---------------|--------------|
| `email` + `name` | `schema:Person` |
| `company`, `organization` | `schema:Organization` |
| `price` + `sku` | `schema:Product` |

## Generating Proxies

### Flask Proxy Generation

```python
from tools.semantic_mapper import ProxyGenerator
from pathlib import Path

generator = ProxyGenerator()
generator.generate_flask_proxy(
    mapping=my_mapping,
    output_dir=Path('./my-proxy')
)
```

This generates:
```
my-proxy/
├── app.py                 # Flask application
├── mapping.yaml          # Mapping specification
├── requirements.txt      # Python dependencies
└── README.md            # Usage instructions
```

### Running the Proxy

```bash
cd my-proxy
pip install -r requirements.txt
python app.py
```

The proxy will:
- ✓ Accept requests at semantic endpoints
- ✓ Forward to source API with authentication
- ✓ Transform responses to semantic format
- ✓ Add semantic headers (Link: describedby, context)
- ✓ Respond to OPTIONS with HTTP Schema Resource

## Examples

### Example 1: Simple User API

See `example-mapping.yaml` for a complete example of mapping a user API.

**Key features:**
- Maps user fields to schema.org Person
- Infers semantic properties automatically
- Generates JSON Schema and JSON-LD context

### Example 2: Stripe Customer API

See `examples/stripe-customers-mapping.yaml` for a real-world example.

**Key features:**
- Complex nested structures (address)
- Field transformations (cents → dollars, Unix → ISO8601)
- Multiple HTTP methods (GET, PUT, POST, DELETE)
- Error handling and response codes

### Example 3: Cross-API Integration

Imagine integrating Stripe, PayPal, and Square payment APIs:

```python
# With semantic mappings, AI tools can generate:

class UnifiedPaymentProvider:
    """Abstraction over multiple payment providers"""

    def charge(self, customer: schema.Person, amount: schema.MonetaryAmount):
        """
        AI understands that:
        - Stripe uses "customer" and "amount" (in cents)
        - PayPal uses "payer" and "total" (in dollars)
        - Square uses "buyer" and "amount_money" (object)

        All map semantically to the same concepts!
        """
        pass
```

## Best Practices

### 1. Start with High-Value Endpoints

Don't try to map an entire API at once. Start with:
- Most frequently used endpoints
- Endpoints you're currently integrating
- Endpoints with well-defined schemas

### 2. Use Standard Vocabularies

Prefer well-known vocabularies:
- **schema.org** for general concepts (Person, Organization, Product)
- **FOAF** for social data
- **Dublin Core** for metadata
- **Domain-specific** only when necessary

### 3. Progressive Enhancement

Start minimal, add richness over time:

**Phase 1:** Basic structure mapping
```yaml
fields:
  - source: "$.name"
    semantic: "name"
    type: "string"
```

**Phase 2:** Add semantics
```yaml
fields:
  - source: "$.name"
    semantic: "name"
    semantic_property: "schema:name"  # Added
    type: "string"
```

**Phase 3:** Add transformations
```yaml
fields:
  - source: "$.name"
    semantic: "name"
    semantic_property: "schema:name"
    type: "string"
    transform: "titleCase"  # Added
```

### 4. Document Your Mappings

Include rich descriptions:
```yaml
- source: "$.balance"
  semantic: "accountBalance"
  semantic_property: "stripe:balance"
  description: |
    Customer's current account balance in dollars.
    Negative values indicate credit, positive indicate debt.
    Transformed from cents in source API.
  transform: "centsToDollars"
```

### 5. Test Thoroughly

Create validation test cases:
```yaml
validation:
  testCases:
    - name: "Retrieve customer with address"
      endpoint: "/customers/cus_123"
      method: GET
      expectedResponse:
        status: 200
        bodyPattern:
          email: "^[^@]+@[^@]+$"
          address:
            postalCode: "^\\d{5}$"
```

### 6. Share and Collaborate

- Publish mappings to community registry
- Use semantic versioning for mappings
- Provide examples and documentation
- Accept community contributions

## Benefits for AI Coding Tools

### For Claude Code Specifically

With semantic mappings, I can:

1. **Understand APIs instantly**
   - No documentation searching needed
   - OPTIONS request reveals everything
   - Semantic types explain meaning, not just structure

2. **Generate perfect code**
   ```typescript
   // I generate this with zero guesswork:
   interface Customer {
     id: string;              // schema:identifier
     email: string;           // schema:email
     address: PostalAddress;  // schema:address → schema:PostalAddress
   }
   ```

3. **Reason across APIs**
   ```python
   # I understand these are semantically equivalent:
   stripe_customer.email    # schema:email
   shopify_customer.email   # schema:email
   paypal_payer.email       # schema:email

   # And can generate unified interfaces automatically
   ```

4. **Validate before execution**
   - Check requests against schemas before sending
   - Prevent runtime errors
   - Suggest corrections

5. **Handle errors intelligently**
   - Know all possible response codes
   - Generate comprehensive error handling
   - Suggest retry strategies

### Example AI Workflow

```
User: "Integrate with the Stripe API to charge customers"

Claude (with semantic mapping):
1. Fetches semantic mapping for Stripe
2. Understands Customer → schema:Person
3. Understands Charge → schema:PaymentAction
4. Generates typed client code
5. Adds proper error handling
6. Suggests testing approach

User: "Now add PayPal support"

Claude:
1. Fetches semantic mapping for PayPal
2. Recognizes both use schema:PaymentAction
3. Generates unified payment interface
4. Adapters for both providers
5. Automatic failover logic

This is impossible without semantic understanding!
```

## FAQ

### Q: Do I need to modify the original API?

**A:** No! That's the whole point. You create a mapping specification and deploy a proxy. The original API remains unchanged.

### Q: What if the API doesn't have an OpenAPI spec?

**A:** You can create the mapping manually or write a simple JSON Schema describing the response format. The tool can work with either.

### Q: Can I map only some endpoints?

**A:** Absolutely. Map the endpoints you actually use. No need to map the entire API.

### Q: How do I handle authentication?

**A:** The proxy forwards authentication headers by default. You can configure this in the mapping:

```yaml
authentication:
  type: bearer
  passthrough: true
  transform:
    from: "Authorization"
    to: "X-API-Key"
```

### Q: What about rate limiting?

**A:** The proxy respects source API rate limits by default. You can also add proxy-level caching:

```yaml
configuration:
  caching:
    enabled: true
    ttl:
      options: 3600
      schemas: 86400
```

### Q: Can I use this in production?

**A:** Yes! The generated proxies are production-ready. Consider:
- Containerizing with Docker
- Using proper authentication/authorization
- Adding monitoring and logging
- Caching aggressively
- Load balancing for scale

### Q: How do I share my mappings?

**A:** We're establishing a community registry. For now:
1. Publish to GitHub
2. Share in the semantic-http-spec discussions
3. Submit PRs to the examples/ directory

### Q: What if the API changes?

**A:** Update your mapping and redeploy the proxy. Include version pinning:

```yaml
metadata:
  apiVersion: "2023-10-16"  # Stripe API version
  mappingVersion: "1.2.0"   # Your mapping version
```

## Next Steps

1. **Try the examples**
   ```bash
   python tools/semantic_mapper.py
   cd example-proxy && python app.py
   ```

2. **Map your own API**
   - Start with one endpoint
   - Test with the generated proxy
   - Iterate and improve

3. **Share your work**
   - Publish your mappings
   - Help build the community
   - Contribute to the tools

4. **Explore advanced features**
   - Complex transformations
   - Multi-endpoint mappings
   - Custom vocabularies
   - Client generation

## Resources

- [Semantic HTTP Spec](README.md)
- [Mapping Specification Format](mapping-spec-format.yaml)
- [Tool Architecture](MAPPING_TOOL_ARCHITECTURE.md)
- [Stripe Example](examples/stripe-customers-mapping.yaml)
- [Tool Source Code](tools/semantic_mapper.py)

## Contributing

We welcome contributions!

- Report issues
- Submit example mappings
- Improve the tools
- Enhance documentation
- Share use cases

Let's build the semantic web together, one API at a time!
