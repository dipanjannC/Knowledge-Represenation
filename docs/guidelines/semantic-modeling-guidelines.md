# Semantic Modeling Guidelines

Guidelines for creating effective semantic models for intelligent systems, LLMs, and agentic workflows.

## Core Principles

1. **Clarity** - Clear names, avoid ambiguity, document thoroughly
2. **Consistency** - Follow naming conventions, align with standards
3. **Extensibility** - Modular design, separate core from extensions
4. **Reusability** - Build on existing ontologies, create reusable patterns

## Design Process

### 1. Requirements

- Identify concepts, relationships, and use cases
- Engage stakeholders and domain experts
- Define scope and boundaries

### 2. Conceptual Modeling

- Create concept hierarchies
- Define properties (object and data)
- Specify constraints and axioms

### 3. Implementation

- Use tools like Protégé or TopBraid
- Implement in OWL/RDF
- Test competency questions and validate consistency

## Best Practices

### OWL

**Classes:**

```turtle
:Person a owl:Class ;
    rdfs:label "Person"@en ;
    rdfs:comment "A human being"@en .
```

**Properties:**

```turtle
:hasCapability a owl:ObjectProperty ;
    rdfs:domain :Agent ; rdfs:range :Capability .
```

**Constraints:**

```turtle
:Human owl:disjointWith :SoftwareAgent .
```

### RDF/RDFS

```turtle
:john_doe a :Person ;
    :hasName "John Doe" ;
    :worksFor :company_xyz .
```

### JSON-LD

```json
{
  "@context": {"@vocab": "http://example.org/ontology#"},
  "@type": "Person",
  "@id": "john_doe",
  "name": "John Doe"
}
```

## AI/ML Integration

### LLMs

- Clear taxonomies with rich descriptions
- Consistent naming patterns
- Descriptive labels for semantic embeddings

### Agentic Systems

**Tool Modeling:**

```turtle
:WebSearchTool a :Tool ;
    :hasCapability :InformationRetrieval ;
    :requires :InternetAccess .
```

**Workflow Modeling:**

```turtle
:DataAnalysisWorkflow a :Workflow ;
    :hasStep :DataCollection, :DataCleaning, :Analysis .
```

### Knowledge Graphs

- Use stable URIs and sameAs links
- Support entity resolution

```sparql
SELECT ?agent ?capability
WHERE { ?agent :hasCapability ?capability . }
```

## Validation

- Use reasoners for consistency checking
- Test competency questions
- Optimize for common query patterns

```sparql
# Example: Find agent capabilities
SELECT ?capability WHERE { :agentX :hasCapability ?capability . }
```

## Common Patterns

**Capability Pattern:**

```turtle
:Agent rdfs:subClassOf [
    owl:onProperty :hasCapability ;
    owl:someValuesFrom :Capability ] .
```

**Process Pattern:**

```turtle
:Process a owl:Class .
:hasInput a owl:ObjectProperty .
:hasOutput a owl:ObjectProperty .
```

## Avoid

- God classes (overly broad)
- Deep hierarchies (>7 levels)
- Ambiguous properties

## Documentation

- Clear descriptions for all classes/properties
- Include usage examples
- Use semantic versioning
- Document design decisions

## Tools

**Development:** Protégé, TopBraid Composer, WebVOWL
**Validation:** HermiT, Pellet, SHACL validators
**Publishing:** WIDOCO, OntoGraf
