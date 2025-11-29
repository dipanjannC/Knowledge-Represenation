import os
import json
from rdflib import Graph, RDF, RDFS, OWL
from litellm import completion


class OntologyExtractor:
    """Extracts entities from RDF graphs."""
    
    def __init__(self, graph_path):
        self.graph_path = graph_path
        self.graph = None
        self.entities = {"classes": [], "properties": []}
    
    def load_graph(self):
        """Load the RDF graph from file."""
        self.graph = Graph()
        self.graph.parse(self.graph_path, format="turtle")
    
    def extract_entities(self):
        """Extract classes and properties from the graph."""
        if not self.graph:
            self.load_graph()
        
        self._extract_classes()
        self._extract_properties()
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
    
    def __init__(self, model="gemini/gemini-1.5-flash"):
        self.model = model
    
    def generate_alignments(self, entities, framework, max_entities=10):
        """Generate alignment suggestions using LLM."""
        framework_context = FrameworkContext.get_context(framework)
        
        # Prepare entity list for prompt
        class_list = "\n".join([
            f"- {e['label']}: {e['comment']}" 
            for e in entities["classes"][:max_entities]
        ])
        
        prompt = self._build_prompt(framework, framework_context, class_list)
        
        try:
            response = completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            return self._parse_response(content)
        except Exception as e:
            print(f"Error calling LLM: {e}")
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
    
    def __init__(self, framework):
        self.framework = framework
        self.prefixes = FrameworkContext.get_prefixes(framework)
    
    def generate_ttl(self, alignments, output_path):
        """Generate TTL file from alignment suggestions."""
        ttl_content = self._build_header()
        ttl_content += self._build_alignments(alignments)
        
        with open(output_path, 'w') as f:
            f.write(ttl_content)
        
        print(f"Generated alignment file: {output_path}")
    
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
    
    def __init__(self, framework="gufo", model="gemini/gemini-1.5-flash"):
        self.framework = framework
        self.model = model
        self.extractor = None
        self.llm_generator = LLMAlignmentGenerator(model)
        self.ttl_generator = TTLGenerator(framework)
    
    def align(self, graph_path, output_path):
        """Execute the full alignment workflow."""
        # Extract entities
        print("Extracting entities from composite graph...")
        self.extractor = OntologyExtractor(graph_path)
        entities = self.extractor.extract_entities()
        print(f"Found {len(entities['classes'])} classes and {len(entities['properties'])} properties")
        
        # Generate alignments
        print(f"\nGenerating alignments with {self.model} for framework: {self.framework}")
        alignments = self.llm_generator.generate_alignments(entities, self.framework)
        print(f"\nGenerated {len(alignments.get('alignments', []))} alignment suggestions")
        
        # Create TTL file
        print("\nCreating TTL file...")
        self.ttl_generator.generate_ttl(alignments, output_path)
        
        print("\nDone! You can now run align_graph.py to use these alignments.")


def main():
    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: No API key found!")
        print("Please set GEMINI_API_KEY or GOOGLE_API_KEY environment variable.")
        print("Example: export GEMINI_API_KEY='your-key-here'")
        return
    
    # Configuration
    framework = "gufo"  # Options: "fibo", "gufo", "saref"
    model = "gemini/gemini-1.5-flash"  # LLM model to use
    
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    composite_graph_path = os.path.join(project_root, "build", "data", "composite_knowledge_graph.ttl")
    output_dir = os.path.join(project_root, "build", "alignment", framework)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "llm_generated_alignment.ttl")
    
    # Execute alignment
    aligner = OntologyAligner(framework=framework, model=model)
    aligner.align(composite_graph_path, output_path)


if __name__ == "__main__":
    main()
