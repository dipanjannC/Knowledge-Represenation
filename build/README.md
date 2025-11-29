# Build Directory

This directory contains scripts for building and aligning knowledge graphs from domain-specific ontologies.

## Overview

The build system provides two workflows:
1. **Manual Workflow**: Combine ontologies and align with standard frameworks
2. **LLM-Assisted Workflow**: Automatically generate alignment mappings using AI

## Scripts

### `build_graph.py`
Combines selected domain-specific TTL files into a single composite knowledge graph.

**Input**: Domain-specific TTL files from `examples/domain-specific/`  
**Output**: `data/composite_knowledge_graph.ttl`  
**Purpose**: Creates a unified graph from modular ontology components

### `llm_align.py`
Uses an LLM to automatically generate alignment mappings between the composite ontology and standard frameworks.

**Architecture**: Class-based modular design
- `OntologyExtractor`: Extracts entities from RDF graphs
- `FrameworkContext`: Manages framework metadata (FIBO, gUFO, SAREF)
- `LLMAlignmentGenerator`: Generates alignments using LLM
- `TTLGenerator`: Creates TTL alignment files
- `OntologyAligner`: Main orchestrator

**Input**: `data/composite_knowledge_graph.ttl`  
**Output**: `alignment/{framework}/llm_generated_alignment.ttl`  
**Configuration**: 
- `framework`: "fibo", "gufo", or "saref"
- `model`: LLM model (default: "gemini/gemini-1.5-flash")

**Requirements**: Set `GEMINI_API_KEY` or `GOOGLE_API_KEY` environment variable

## Directories

- **`data/`**: Generated knowledge graphs
  - `composite_knowledge_graph.ttl`: Combined ontology
  - `aligned_knowledge_graph.ttl`: Ontology aligned with standard framework
  
- **`alignment/`**: Framework metadata and alignment files
  - `framework_metadata.json`: URLs to standard ontologies (FIBO, gUFO, SAREF)
  - `fibo/`, `gufo/`, `saref/`: Framework-specific directories
    - Contains LLM-generated or manual alignment TTL files

## Usage

### Manual Workflow
1. Run `build_graph.py` to create the composite graph
2. Manually create alignment files in `alignment/{framework}/`
3. Run your alignment script to generate the final aligned graph

### LLM-Assisted Workflow (Recommended)

```bash
# Step 1: Build composite graph
python build/build_graph.py

# Step 2: Set your Gemini API key
export GEMINI_API_KEY='your-gemini-api-key'

# Step 3: Configure framework in llm_align.py
# Edit the script to set:
#   framework = "gufo"  # or "fibo", "saref"
#   model = "gemini/gemini-1.5-flash"

# Step 4: Generate alignment mappings
python build/llm_align.py

# Output: alignment/{framework}/llm_generated_alignment.ttl
```

## Supported Frameworks

### FIBO (Financial Industry Business Ontology)
- **Domain**: Finance, banking, securities
- **Concepts**: Accounts, Transactions, Legal Entities, Financial Instruments
- **Use for**: Finance-related ontologies

### gUFO (Unified Foundational Ontology)
- **Domain**: Foundational categories
- **Concepts**: FunctionalComplex, Event, Role, Quality
- **Use for**: General-purpose ontologies, IoT, systems

### SAREF (Smart Applications REFerence)
- **Domain**: IoT and smart systems
- **Concepts**: Device, Sensor, Actuator, Measurement
- **Use for**: Smart home, IoT ontologies

## How LLM Alignment Works

1. **Entity Extraction**: Parses composite graph to extract classes and properties
2. **Context Building**: Loads framework-specific context and examples
3. **LLM Prompting**: Sends entities and framework info to LLM
4. **Mapping Generation**: LLM suggests `owl:equivalentClass` or `rdfs:subClassOf` mappings
5. **TTL Output**: Generates properly formatted alignment file

## Configuration

### Changing Framework
Edit `llm_align.py`:
```python
framework = "fibo"  # Options: "fibo", "gufo", "saref"
```

### Changing LLM Model
Edit `llm_align.py`:
```python
model = "gemini/gemini-1.5-pro"  # Or other litellm-supported models
```

### Adding New Frameworks
1. Add framework context to `FrameworkContext.CONTEXTS`
2. Add prefix mappings to `FrameworkContext.PREFIX_MAP`
3. Add URL to `alignment/framework_metadata.json`

## Benefits

**Automated**: No manual alignment creation needed  
**Consistent**: Uses standard ontology knowledge  
**Flexible**: Easy to switch between frameworks  
**Modular**: Clean class-based architecture  
**Extensible**: Simple to add new frameworks or models
