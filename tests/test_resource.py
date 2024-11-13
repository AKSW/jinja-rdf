from rdflib import Graph
from jinja_rdf.resource import Resource
from simpsons_rdf import simpsons, SIM, FAM
from rdflib.namespace import FOAF
import jinja2

def test_resource():
    homer = Resource(simpsons.graph, SIM.Homer)
    environment = jinja2.Environment()
    template = environment.from_string("Hello, {{homer[\"FOAF.name\"] }}!")
    assert template.render(homer=homer) == "Hello, Homer"
