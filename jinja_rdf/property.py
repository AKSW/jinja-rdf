from rdflib import URIRef
from rdflib.resource import Resource as RDFResource
from .resource import Resource

def property(resource: RDFResource, property: str | URIRef):
    return Resource._cast(None, resource)[property]

def inv_property(resource: RDFResource, property: str | URIRef):
    return Resource._cast(None, resource).subjects(property)
