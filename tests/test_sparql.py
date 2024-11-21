from jinja_rdf.rdf_resource import RDFResource as Resource
from jinja_rdf.sparql_query import sparql_query
from simpsons_rdf import simpsons, SIM, FAM
from rdflib.namespace import FOAF
from rdflib import Literal
from undent import undent


def test_sparql():
    homer = Resource(simpsons.graph, SIM.Homer)
    bindings = sparql_query(homer, undent("""
        select ?resourceUri ?name {
            ?resourceUri foaf:name ?name
        }
    """))
    for row in bindings:
        assert row["resourceUri"] == SIM.Homer
        assert row["name"] == Literal("Homer Simpson")
