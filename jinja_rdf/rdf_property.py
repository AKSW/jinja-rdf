from rdflib import URIRef
from rdflib.resource import Resource as RDFLibResource
from rdflib.util import from_n3


def rdf_property(resource: RDFLibResource, property: str | URIRef):
    if isinstance(property, str):
        property = from_n3(property)
    return resource.objects(property)


def rdf_inverse_property(resource: RDFLibResource, property: str | URIRef):
    if isinstance(property, str):
        property = from_n3(property)
    return resource.subjects(property)
