import pytest
from rdflib import Graph
from jinja_rdf.rdf_resource import RDFResource as Resource
from jinja_rdf.rdf_resource import cast as rdf_cast
from jinja_rdf.rdf_property import rdf_property, rdf_inverse_property
from simpsons_rdf import simpsons, SIM, FAM
from rdflib.namespace import FOAF
from rdflib.resource import Resource as RDFLibResource
from rdflib import Literal
from undent import undent
import jinja2


def test_resource():
    homer = Resource(simpsons.graph, SIM.Homer)
    name = list(homer[FOAF.name.n3()])
    assert Literal("Homer Simpson") in name


def test_resource_property_n3():
    homer = Resource(simpsons.graph, SIM.Homer)
    name = list(rdf_property(homer, FOAF.name.n3()))
    assert Literal("Homer Simpson") in name


def test_resource_property():
    homer = Resource(simpsons.graph, SIM.Homer)
    print(type(homer))
    print(FOAF.name)
    print(type(FOAF.name))
    name = list(rdf_property(homer, FOAF.name))
    assert Literal("Homer Simpson") in name


def test_inverse_property_n3():
    homer = Resource(simpsons.graph, SIM.Homer)
    kids = list(rdf_inverse_property(homer, FAM.hasFather.n3()))
    assert Resource(simpsons.graph, SIM.Bart) in kids
    assert Resource(simpsons.graph, SIM.Lisa) in kids
    assert Resource(simpsons.graph, SIM.Maggie) in kids


def test_inverse_property():
    homer = Resource(simpsons.graph, SIM.Homer)
    kids = list(rdf_inverse_property(homer, FAM.hasFather))
    assert Resource(simpsons.graph, SIM.Bart) in kids
    assert Resource(simpsons.graph, SIM.Lisa) in kids
    assert Resource(simpsons.graph, SIM.Maggie) in kids
