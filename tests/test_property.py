from jinja_rdf.rdf_resource import RDFResource as Resource
from jinja_rdf.rdf_property import (
    rdf_property,
    rdf_inverse_properties,
)
from simpsons_rdf import simpsons, SIM, FAM
from rdflib.namespace import FOAF
from rdflib import Literal
from .helper import mock_context


def test_resource_property_n3():
    ctx = mock_context()
    homer = Resource(simpsons.graph, SIM.Homer)
    name = rdf_property(ctx, homer, FOAF.name.n3())
    assert Literal("Homer Simpson") == name


def test_resource_property():
    ctx = mock_context()
    homer = Resource(simpsons.graph, SIM.Homer)
    name = rdf_property(ctx, homer, FOAF.name)
    assert Literal("Homer Simpson") == name


def test_inverse_property_n3():
    ctx = mock_context()
    homer = Resource(simpsons.graph, SIM.Homer)
    kids = list(rdf_inverse_properties(ctx, homer, FAM.hasFather.n3()))
    assert Resource(simpsons.graph, SIM.Bart) in kids
    assert Resource(simpsons.graph, SIM.Lisa) in kids
    assert Resource(simpsons.graph, SIM.Maggie) in kids


def test_inverse_property():
    ctx = mock_context()
    homer = Resource(simpsons.graph, SIM.Homer)
    kids = list(rdf_inverse_properties(ctx, homer, FAM.hasFather))
    assert Resource(simpsons.graph, SIM.Bart) in kids
    assert Resource(simpsons.graph, SIM.Lisa) in kids
    assert Resource(simpsons.graph, SIM.Maggie) in kids


def test_chained_property():
    ctx = mock_context()
    homer = Resource(simpsons.graph, SIM.Homer)
    kids = list(rdf_inverse_properties(ctx, homer, FAM.hasFather))
    names = []
    for kid in kids:
        assert isinstance(kid, Resource)
        names.append(*[str(n) for n in kid[FOAF.name.n3()]])

    assert "Lisa Simpson" in names
    assert "Maggie Simpson" in names
    assert "Bart Simpson" in names
