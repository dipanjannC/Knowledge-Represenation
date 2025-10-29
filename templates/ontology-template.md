# Ontology Template

## Basic Information
- **Name**: [Ontology Name]
- **Version**: [Version Number]
- **Purpose**: [Brief description of what this ontology models]
- **Domain**: [Target domain or application area]
- **Author**: [Creator name/organization]
- **Date**: [Creation/modification date]

## Namespace Declaration
```turtle
@prefix : <http://example.org/[domain]#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
```

## Ontology Declaration
```turtle
: rdf:type owl:Ontology ;
  rdfs:label "[Ontology Name]"@en ;
  rdfs:comment "[Detailed description]"@en ;
  owl:versionInfo "[Version]" .
```

## Core Classes
```turtle
# Main domain class
:[MainClass] rdf:type owl:Class ;
    rdfs:label "[Class Label]"@en ;
    rdfs:comment "[Class description]"@en .

# Subclasses
:[SubClass1] rdf:type owl:Class ;
    rdfs:subClassOf :[MainClass] ;
    rdfs:label "[Subclass Label]"@en ;
    rdfs:comment "[Subclass description]"@en .
```

## Properties

### Object Properties
```turtle
:[objectProperty] rdf:type owl:ObjectProperty ;
    rdfs:domain :[DomainClass] ;
    rdfs:range :[RangeClass] ;
    rdfs:label "[property label]"@en ;
    rdfs:comment "[property description]"@en .
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