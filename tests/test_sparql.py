from jinja_rdf.rdf_resource import RDFResource as Resource
from jinja_rdf.sparql_query import sparql_query
from simpsons_rdf import simpsons, SIM
from rdflib.namespace import FOAF
from rdflib import Literal
from undent import undent


def test_sparql_select():
    homer = Resource(simpsons.graph, SIM.Homer)
    bindings = sparql_query(
        homer,
        undent("""
        select ?resourceIri ?name {
            ?resourceIri foaf:name ?name
        }
    """),
    )
    for row in bindings:
        assert row["resourceIri"] == SIM.Homer
        assert row["name"] == Literal("Homer Simpson")


def test_sparql_construct():
    homer = Resource(simpsons.graph, SIM.Homer)
    graph = sparql_query(
        homer,
        undent("""
        construct {
            ?resourceIri foaf:name ?name
        } where {
            ?resourceIri foaf:name ?name
        }
    """),
    )
    for s, p, o in graph:
        assert s == SIM.Homer
        assert p == FOAF.name
        assert o == Literal("Homer Simpson")
