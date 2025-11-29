"""LLM-based ontology alignment system."""

import json
from pathlib import Path
from rdflib import Graph, RDF, RDFS, OWL
from litellm import completion

from utils import Logger, FileManager, ConfigManager


class OntologyExtractor:
    """Extracts entities from RDF graphs."""
    
    def __init__(self, graph_path: Path, logger: Logger):
        self.graph_path = graph_path
        self.logger = logger
        self.graph = None
        self.entities = {"classes": [], "properties": []}
    
    def load_graph(self):
        """Load the RDF graph from file."""
        self.logger.info(f"Loading graph from: {self.graph_path}")
        self.graph = Graph()
        self.graph.parse(str(self.graph_path), format="turtle")
    
    def extract_entities(self):
        """Extract classes and properties from the graph."""
        if not self.graph:
            self.load_graph()
        
        self._extract_classes()
        self._extract_properties()
        
        self.logger.info(
            f"Extracted {len(self.entities['classes'])} classes and "
            f"{len(self.entities['properties'])} properties"
        )
        return self.entities
    
    def _extract_classes(self):
        """Extract OWL classes."""
        for s in self.graph.subjects(RDF.type, OWL.Class):
            label = self._extract_label(str(s))
            comment = self.graph.value(s, RDFS.comment)
            self.entities["classes"].append({
                "uri": str(s),
                "label": label,
                "comment": str(comment) if comment else ""
            })
    
    def _extract_properties(self):
        """Extract OWL properties."""
        property_types = [OWL.ObjectProperty, OWL.DatatypeProperty]
        
        for prop_type in property_types:
            for s in self.graph.subjects(RDF.type, prop_type):
                label = self._extract_label(str(s))
                comment = self.graph.value(s, RDFS.comment)
                self.entities["properties"].append({
                    "uri": str(s),
                    "label": label,
                    "comment": str(comment) if comment else ""
                })
    
    @staticmethod
    def _extract_label(uri):
        """Extract label from URI."""
        return uri.split("#")[-1] if "#" in uri else uri.split("/")[-1]


class FrameworkContext:
    """Manages framework-specific context and metadata."""
    
    CONTEXTS = {
        "fibo": """FIBO (Financial Industry Business Ontology) is a standard for financial concepts including:
- Accounts, Transactions, Payments
- Legal Entities, Organizations
- Financial Instruments, Securities
- Assets, Liabilities
Key namespaces: fibo-fnd-acc-aeq (Accounting), fibo-be-le-lp (Legal Persons), fibo-fnd-pas-psn (Payments)""",
        
        "gufo": """gUFO (Unified Foundational Ontology) provides foundational categories:
- FunctionalComplex: Objects with functions (devices, systems)
- Event: Occurrences in time (transactions, actions)
- Role: Context-dependent classifications
- Quality: Attributes and properties
Key namespace: http://purl.org/nemo/gufo#""",
        
        "saref": """SAREF (Smart Applications REFerence) is for IoT and smart systems:
- Device: Physical or virtual devices
- Sensor: Measurement devices
- Actuator: Control devices
- Measurement, Property, Unit
Key namespace: https://saref.etsi.org/core/"""
    }
    
    PREFIX_MAP = {
        "fibo": {
            "fibo-fnd-acc-aeq": "https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/AccountingEquity/",
            "fibo-be-le-lp": "https://spec.edmcouncil.org/fibo/ontology/BE/LegalEntities/LegalPersons/",
            "fibo-fnd-pas-psn": "https://spec.edmcouncil.org/fibo/ontology/FND/ProductsAndServices/PaymentsAndSchedules/"
        },
        "gufo": {
            "gufo": "http://purl.org/nemo/gufo#"
        },
        "saref": {
            "saref": "https://saref.etsi.org/core/"
        }
    }
    
    @classmethod
    def get_context(cls, framework):
        """Get context description for a framework."""
        return cls.CONTEXTS.get(framework, "")
    
    @classmethod
    def get_prefixes(cls, framework):
        """Get prefix mappings for a framework."""
        return cls.PREFIX_MAP.get(framework, {})


class LLMAlignmentGenerator:
    """Generates alignment mappings using an LLM."""
    
    def __init__(self, model: str, logger: Logger):
        self.model = model
        self.logger = logger
    
    def generate_alignments(self, entities, framework, max_entities=10):
        """Generate alignment suggestions using LLM."""
        framework_context = FrameworkContext.get_context(framework)
        
        # Prepare entity list for prompt
        class_list = "\n".join([
            f"- {e['label']}: {e['comment']}" 
            for e in entities["classes"][:max_entities]
        ])
        
        prompt = self._build_prompt(framework, framework_context, class_list)
        
        self.logger.info(f"Generating alignments with {self.model} for framework: {framework}")
        
        try:
            response = completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            alignments = self._parse_response(content)
            
            self.logger.info(f"Generated {len(alignments.get('alignments', []))} alignment suggestions")
            return alignments
            
        except Exception as e:
            self.logger.error(f"Error calling LLM: {e}")
            return {"alignments": []}
    
    @staticmethod
    def _build_prompt(framework, context, class_list):
        """Build the LLM prompt."""
        return f"""You are an ontology alignment expert. Given these custom ontology classes and a target framework, suggest alignment mappings.

Target Framework: {framework.upper()}
{context}

Custom Ontology Classes:
{class_list}

For each class, suggest ONE of:
1. owl:equivalentClass - if semantically identical
2. rdfs:subClassOf - if it's a specialization
3. SKIP - if no good match

Respond in JSON format:
{{
  "alignments": [
    {{"custom_class": "ClassName", "relation": "owl:equivalentClass", "target": "framework:TargetClass", "confidence": "high/medium/low"}}
  ]
}}

Only include alignments with medium or high confidence."""
    
    @staticmethod
    def _parse_response(content):
        """Parse LLM response and extract JSON."""
        # Extract JSON from markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        return json.loads(content)


class TTLGenerator:
    """Generates TTL files from alignment data."""
    
    def __init__(self, framework: str, logger: Logger):
        self.framework = framework
        self.logger = logger
        self.prefixes = FrameworkContext.get_prefixes(framework)
    
    def generate_ttl(self, alignments, output_path: Path):
        """Generate TTL file from alignment suggestions."""
        self.logger.info("Creating TTL file...")
        
        ttl_content = self._build_header()
        ttl_content += self._build_alignments(alignments)
        
        with open(output_path, 'w') as f:
            f.write(ttl_content)
        
        self.logger.info(f"Generated alignment file: {output_path}")
    
    def _build_header(self):
        """Build TTL header with prefixes."""
        header = """@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
"""
        
        for prefix, uri in self.prefixes.items():
            header += f"@prefix {prefix}: <{uri}> .\n"
        
        header += "\n# LLM-Generated Alignments\n\n"
        return header
    
    def _build_alignments(self, alignments):
        """Build alignment triples."""
        content = ""
        
        for alignment in alignments.get("alignments", []):
            custom_class = alignment.get("custom_class", "")
            relation = alignment.get("relation", "")
            target = alignment.get("target", "")
            confidence = alignment.get("confidence", "")
            
            if custom_class and relation and target:
                cls = self._extract_class_name(custom_class)
                content += f"# Confidence: {confidence}\n"
                content += f":{cls} {relation} {target} .\n\n"
        
        return content
    
    @staticmethod
    def _extract_class_name(custom_class):
        """Extract class name from prefixed or unprefixed string."""
        if ":" in custom_class:
            return custom_class.split(":", 1)[1]
        return custom_class


class OntologyAligner:
    """Main orchestrator for ontology alignment process."""
    
    def __init__(self, framework: str, model: str, logger: Logger, file_manager: FileManager):
        self.framework = framework
        self.model = model
        self.logger = logger
        self.file_manager = file_manager
        
        self.extractor = None
        self.llm_generator = LLMAlignmentGenerator(model, logger)
        self.ttl_generator = TTLGenerator(framework, logger)
    
    def align(self, graph_path: Path, output_path: Path):
        """Execute the full alignment workflow."""
        # Validate input file
        self.file_manager.validate_file(graph_path, "Composite graph")
        
        # Extract entities
        self.extractor = OntologyExtractor(graph_path, self.logger)
        entities = self.extractor.extract_entities()
        
        # Generate alignments
        alignments = self.llm_generator.generate_alignments(entities, self.framework)
        
        # Ensure output directory exists
        self.file_manager.ensure_dir_exists(output_path.parent)
        
        # Create TTL file
        self.ttl_generator.generate_ttl(alignments, output_path)
        
        self.logger.info("Alignment process completed successfully!")


def main():
    """Main entry point."""
    # Set up utilities
    logger = Logger()
    file_manager = FileManager()
    
    try:
        # Validate API key
        ConfigManager.validate_api_key()
        
        # Configuration
        framework = "gufo"  # Options: "fibo", "gufo", "saref"
        model = "gemini/gemini-1.5-flash"  # LLM model to use
        
        # Validate framework
        ConfigManager.validate_framework(framework)
        
        # Get paths
        composite_graph_path = file_manager.get_composite_graph_path()
        output_path = file_manager.get_alignment_output_path(framework)
        
        # Execute alignment
        aligner = OntologyAligner(framework, model, logger, file_manager)
        aligner.align(composite_graph_path, output_path)
        
    except (ValueError, FileNotFoundError) as e:
        logger.error(str(e))
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
