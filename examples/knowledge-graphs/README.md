# Knowledge Graph Example: AI Research Domain

This directory contains examples of knowledge graphs for the AI research domain, demonstrating how to represent entities, relationships, and complex knowledge structures.

## Files

### research-network.ttl
A comprehensive knowledge graph representing:
- Researchers and their affiliations
- Publications and citations
- Research topics and methodologies
- Collaborations and influence networks

### Query Examples

#### Find all papers by a specific researcher
```sparql
PREFIX : <http://example.org/research#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?paper ?title WHERE {
    :researcher_smith :hasPublication ?paper .
    ?paper :hasTitle ?title .
}
```

#### Find researchers working on specific topics
```sparql
PREFIX : <http://example.org/research#>

SELECT ?researcher ?name WHERE {
    ?researcher :researchesIn :machine_learning .
    ?researcher :hasName ?name .
}
```

#### Find collaboration networks
```sparql
PREFIX : <http://example.org/research#>

SELECT ?author1 ?author2 ?paper WHERE {
    ?paper :hasAuthor ?author1, ?author2 .
    FILTER(?author1 != ?author2)
}
```

## Applications for Agentic Systems

1. **Research Assistant Agents**: Can query the knowledge graph to find relevant papers, researchers, and trends
2. **Collaboration Recommendation**: Identify potential research collaborators based on shared interests
3. **Citation Analysis**: Analyze research impact and influence patterns
4. **Topic Evolution**: Track how research topics evolve over time