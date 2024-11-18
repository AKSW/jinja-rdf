from rdflib import URIRef
from rdflib.resource import Resource as RDFLibResource
from rdflib.util import from_n3


def rdf_property(resource: RDFLibResource, property: str | URIRef):
    return resource.objects(from_n3(property))


def rdf_inverse_property(resource: RDFLibResource, property: str | URIRef):
    return resource.subjects(from_n3(property))
