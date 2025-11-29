# Standard Ontologies Research

This document summarizes standard ontologies relevant to the domain-specific examples in this repository. These standards can serve as a reference for extending and aligning the custom ontologies.

## Smart Systems (IoT & Smart Home)

### SAREF (Smart Applications REFerence Ontology)
- **Focus**: Devices, functions, commands, and services in smart applications.
- **Key Features**: Modularity (extensions for energy, buildings, etc.), industry alignment (ETSI standard).
- **Relevance**: Use for modeling device capabilities and functions in `smart-systems`.

### SSN (Semantic Sensor Network) / SOSA (Sensor, Observation, Sample, and Actuator)
- **Focus**: Sensors, observations, actuators, and sampling.
- **Key Features**: W3C standard, lightweight core (SOSA), detailed sensor modeling.
- **Relevance**: Use for detailed modeling of sensors and their data in `smart-systems/sensors.ttl`.

## Finance

### FIBO (Financial Industry Business Ontology)
- **Focus**: Global standard for financial concepts (business entities, processes, loans, securities).
- **Key Features**: Developed by EDM Council and OMG, highly modular, precise definitions.
- **Relevance**: The gold standard for `finance` domain. Align `instruments.ttl`, `organization.ttl`, and `portfolios.ttl` with FIBO concepts.

## Social Bias & Fairness

### Fairness Metrics Ontology (FMO)
- **Focus**: Fairness metrics, use cases, and relationships.
- **Relevance**: Useful for `social-bias/mitigation.ttl` to define metrics for algorithmic fairness.

### Ontology for Ethical AI Principles (AIPO)
- **Focus**: Ethical AI principles and their relationships.
- **Relevance**: Broader context for `social-bias/biases.ttl`.

### Doc-BiasO
- **Focus**: Vocabulary of biases in fair-ML literature.
- **Relevance**: Can help expand the list of bias types in `social-bias/biases.ttl`.
