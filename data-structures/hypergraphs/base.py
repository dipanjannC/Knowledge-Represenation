graph = {
    "e1" : ["v1", "v2", "v3"],
    "e2" : ["v2", "v4"],
    "e3" : ["v1", "v4", "v5", "v6"],
    }

def print_hypergraph(graph):
    for edge, vertices in graph.items():
        print(f"Hyperedge {edge} connects vertices: {vertices}")


def HyperGraph(graph):
    """A simple hypergraph representation using a dictionary.

    Args:
        graph (dict): A dictionary where keys are hyperedge identifiers and values are lists of vertices.

    Returns:
        dict: The hypergraph representation.
    """

    print("Initial Hypergraph:\n")
    print_hypergraph(graph)

    print("\nModifying Hypergraph:\n")
    # add a new hyperedge
    graph["e4"] = ["v3", "v5"]
    print_hypergraph(graph)

    print("\nAfter removing an edge:\n")
    #remove an edge
    del graph["e2"]
    print_hypergraph(graph)


    print("\nAfter modifications:\n")
    #Modify a Hyperedge
    graph["e1"] = ["v1", "v2"]
    print_hypergraph(graph)


if __name__ == "__main__":
    HyperGraph(graph)

    
    

