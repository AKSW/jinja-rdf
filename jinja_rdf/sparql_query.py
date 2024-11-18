from rdflib import URIRef
from rdflib.resource import Resource as RDFLibResource
from .rdf_resource import RDFResource

def sparql_query(resource: RDFLibResource, query: str):
    graph.query(query)
    return RDFResource._cast(None, resource)[property]
