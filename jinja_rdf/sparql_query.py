from rdflib import URIRef
from rdflib.resource import Resource as RDFLibResource
from rdflib import Graph
from jinja2 import pass_context
from jinja2.runtime import Context


@pass_context
def sparql_query(context: Context, input: RDFLibResource | Graph | URIRef, query: str):
    if isinstance(input, Graph):
        graph = input
        resourceIri = input.identifier
    if isinstance(input, RDFLibResource):
        graph = input.graph
        resourceIri = input.identifier
    if isinstance(input, URIRef):
        graph = context["graph"]
        resourceIri = input
    return graph.query(
        query,
        initBindings={
            "resourceIri": resourceIri,
            "resourceUri": resourceIri,
            "graphIri": graph.identifier,
        },
        initNs=dict(context["namespace_manager"].namespaces()),
    )
