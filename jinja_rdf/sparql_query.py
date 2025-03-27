from rdflib.resource import Resource as RDFLibResource
from rdflib import Graph


def sparql_query(input: RDFLibResource | Graph, query: str):
    if isinstance(input, Graph):
        graph = input
    if isinstance(input, RDFLibResource):
        graph = input.graph
    return graph.query(
        query,
        initBindings={
            "resourceIri": input.identifier,
            "resourceUri": input.identifier,
            "graphIri": graph.identifier,
        },
    )
