# Ontology Template

## Metadata
- **Name**: [Ontology Name]
- **Version**: [Version]
- **Purpose**: [Description]
- **Author**: [Name]

## Namespaces
```turtle
@prefix : <http://example.org/[domain]#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
```

## Ontology
```turtle
: a owl:Ontology ;
  rdfs:label "[Name]"@en ;
  rdfs:comment "[Description]"@en .
```

## Classes
```turtle
:[MainClass] a owl:Class ;
    rdfs:label "[Label]"@en .

:[SubClass] a owl:Class ;
    rdfs:subClassOf :[MainClass] .
```

## Properties
```turtle
:[property] a owl:ObjectProperty ;
    rdfs:domain :[DomainClass] ;
    rdfs:range :[RangeClass] .
```

### Data Properties
```turtle
:[dataProperty] rdf:type owl:DatatypeProperty ;
    rdfs:domain :[DomainClass] ;
    rdfs:range xsd:[datatype] ;
    rdfs:label "[property label]"@en ;
    rdfs:comment "[property description]"@en .
```

## Axioms and Constraints
```turtle
# Disjoint classes
:[Class1] owl:disjointWith :[Class2] .

# Cardinality constraints
:[Class] rdfs:subClassOf 
    [ rdf:type owl:Restriction ;
      owl:onProperty :[property] ;
      owl:cardinality 1 ] .
```

## Example Instances
```turtle
:[instance1] rdf:type :[Class] ;
    :[property] "value" ;
    rdfs:label "[Instance Label]"@en .
```

## Competency Questions
1. What are the main entities in this domain?
2. How do these entities relate to each other?
3. What properties do these entities have?
4. What constraints exist in this domain?

## Usage Notes
- [Guidelines for using this ontology]
- [Integration notes with other ontologies]
- [Known limitations or assumptions]