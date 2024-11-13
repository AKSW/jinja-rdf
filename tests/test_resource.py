from rdflib import Graph
from rdflib_jinja.resource import Resource
from simpsons import graph as simpsons, SIM, FAM
from rdflib.namespace import FOAF
import jinja2

def test_resource():
    homer = Resource(simpsons, SIM.Homer)
    environment = jinja2.Environment()
    template = environment.from_string("Hello, {{homer[\"FOAF.name\"] }}!")
    assert template.render(homer=homer) == "Hello, Homer"
