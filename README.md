# Knowledge Representation - Ontology Alignment System

This project provides an automated ontology alignment system with LLM integration for aligning custom ontologies with standard frameworks (FIBO, gUFO, SAREF).

## Installation

### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/dipanjannC/Knowledge-Represenation.git
cd Knowledge-Represenation

# Create virtual environment and install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

### Manual Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install rdflib litellm
```

## Dependencies

- **rdflib** (>=7.1.1): RDF graph manipulation and parsing
- **litellm** (>=1.80.0): Unified LLM API interface

### Optional Development Dependencies

- **pytest** (>=8.0.0): Testing framework
- **black** (>=24.0.0): Code formatter
- **ruff** (>=0.8.0): Fast Python linter

## Quick Start

1. **Set up API key**:
   ```bash
   export GEMINI_API_KEY='your-gemini-api-key'
   ```

2. **Build composite graph**:
   ```bash
   python build/build_graph.py
   ```

3. **Generate alignments**:
   ```bash
   python build/llm_align.py
   ```

## Project Structure

```
.
├── build/                  # Build scripts and alignment system
│   ├── llm_align.py       # LLM-based alignment generator
│   ├── build_graph.py     # Composite graph builder
│   ├── alignment/         # Framework metadata and alignments
│   └── data/              # Generated graphs
├── examples/              # Domain-specific ontologies
│   └── domain-specific/   # Modular TTL files
├── templates/             # Ontology templates
└── pyproject.toml         # Project dependencies
```

## Features

- **Automated Alignment**: LLM-generated mappings between ontologies
- **Multiple Frameworks**: Support for FIBO, gUFO, and SAREF
- **Modular Architecture**: Clean class-based design
- **Flexible Configuration**: Easy framework and model selection

## Documentation

See [build/README.md](build/README.md) for detailed usage instructions.

## License

MIT License
