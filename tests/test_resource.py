from jinja_rdf.rdf_resource import RDFResource as Resource
from jinja_rdf.rdf_property import rdf_property, rdf_inverse_property, rdf_properties, rdf_inverse_properties
from simpsons_rdf import simpsons, SIM, FAM
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

def test_resource_property_n3():
    homer = Resource(simpsons.graph, SIM.Homer)
    name = rdf_property(homer, FOAF.name.n3())
    assert Literal("Homer Simpson") == name


def test_resource_property():
    homer = Resource(simpsons.graph, SIM.Homer)
    name = rdf_property(homer, FOAF.name)
    assert Literal("Homer Simpson") == name


def test_inverse_property_n3():
    homer = Resource(simpsons.graph, SIM.Homer)
    kids = list(rdf_inverse_properties(homer, FAM.hasFather.n3()))
    assert Resource(simpsons.graph, SIM.Bart) in kids
    assert Resource(simpsons.graph, SIM.Lisa) in kids
    assert Resource(simpsons.graph, SIM.Maggie) in kids


def test_inverse_property():
    homer = Resource(simpsons.graph, SIM.Homer)
    kids = list(rdf_inverse_properties(homer, FAM.hasFather))
    assert Resource(simpsons.graph, SIM.Bart) in kids
    assert Resource(simpsons.graph, SIM.Lisa) in kids
    assert Resource(simpsons.graph, SIM.Maggie) in kids


def test_chained_property():
    homer = Resource(simpsons.graph, SIM.Homer)
    kids = list(rdf_inverse_properties(homer, FAM.hasFather))
    names = []
    for kid in kids:
        assert isinstance(kid, Resource)
        names.append(*[str(n) for n in kid[FOAF.name.n3()]])

    assert "Lisa Simpson" in names
    assert "Maggie Simpson" in names
    assert "Bart Simpson" in names
