import os
from rdflib import Graph

def build_composite_graph(base_dir, output_file):
    """
    Combines selected TTL files into a single composite graph.
    """
    g = Graph()

    # Define the list of files to include
    # Paths are relative to the project root
    files_to_include = [
        # Smart Systems
        "examples/domain-specific/smart-systems/core.ttl",
        "examples/domain-specific/smart-systems/devices.ttl",
        "examples/domain-specific/smart-systems/sensors.ttl",
        "examples/domain-specific/smart-systems/rooms.ttl",
        
        # Personal Finance
        "examples/domain-specific/finance/accounts.ttl",
        "examples/domain-specific/finance/transactions.ttl",
        
        # Social Bias
        "examples/domain-specific/social-bias/biases.ttl"
    ]

    print("Building composite graph...")
    
    for file_path in files_to_include:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            print(f"Parsing: {file_path}")
            try:
                g.parse(full_path, format="turtle")
            except Exception as e:
                print(f"Error parsing {file_path}: {e}")
        else:
            print(f"Warning: File not found: {file_path}")

    print(f"Graph built with {len(g)} triples.")
    
    # Serialize the combined graph
    print(f"Saving to: {output_file}")
    g.serialize(destination=output_file, format="turtle")
    print("Done.")

if __name__ == "__main__":
    # Assuming the script is run from the project root or build directory
    # We'll try to find the project root
    
    current_dir = os.getcwd()
    # If we are in the build dir, go up one level
    if os.path.basename(current_dir) == "build":
        project_root = os.path.dirname(current_dir)
    else:
        project_root = current_dir
        
    output_path = os.path.join(project_root, "build", "data", "composite_knowledge_graph.ttl")
    
    build_composite_graph(project_root, output_path)
