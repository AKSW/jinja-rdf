from rdflib import URIRef
from rdflib.resource import Resource as RDFLibResource
from .rdf_resource import RDFResource

def rdf_property(resource: RDFLibResource, property: str | URIRef):
    return RDFResource._cast(None, resource)[property]

def rdf_inverse_property(resource: RDFLibResource, property: str | URIRef):
    return RDFResource._cast(None, resource).subjects(property)
