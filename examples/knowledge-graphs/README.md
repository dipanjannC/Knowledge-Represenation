# Knowledge Graph Examples

AI research domain knowledge graph demonstrating entities, relationships, and query patterns.

## Contents

**research-network.ttl** - Researchers, publications, citations, collaborations

## Query Examples

**Find papers by researcher:**
```sparql
SELECT ?paper ?title WHERE {
    :researcher_smith :hasPublication ?paper .
    ?paper :hasTitle ?title .
}
```

**Find collaborations:**
```sparql
SELECT ?author1 ?author2 ?paper WHERE {
    ?paper :hasAuthor ?author1, ?author2 .
    FILTER(?author1 != ?author2)
}
```

## Applications

- Research assistant agents for finding papers and trends
- Collaboration recommendation systems
3. **Citation Analysis**: Analyze research impact and influence patterns
4. **Topic Evolution**: Track how research topics evolve over time