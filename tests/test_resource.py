from jinja_rdf.rdf_resource import RDFResource as Resource
from simpsons_rdf import simpsons, SIM
from rdflib.namespace import FOAF
from rdflib import Literal


def test_resource_item_n3():
    homer = Resource(simpsons.graph, SIM.Homer)
    name = list(homer[FOAF.name.n3()])
    assert Literal("Homer Simpson") in name


def test_resource_item_qname():
    homer = Resource(simpsons.graph, SIM.Homer)
    name = list(homer["foaf:name"])
    assert Literal("Homer Simpson") in name


def test_resource_item():
    homer = Resource(simpsons.graph, SIM.Homer)
    name = list(homer[FOAF.name])
    assert Literal("Homer Simpson") in name
