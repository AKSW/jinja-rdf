from rdflib import Graph
from jinja_rdf.resource import Resource
from jinja_rdf.property import property
from simpsons_rdf import simpsons, SIM, FAM
from rdflib.namespace import FOAF
from undent import undent
import jinja2

def test_resource():
    homer = Resource(simpsons.graph, SIM.Homer)
    environment = jinja2.Environment()
    template_str = "Hello, {{ homer[\"" + FOAF.name.n3() + "\"] | join(', ') }}!"
    template_str = "Hello, {{ homer[\"" + FOAF.name.n3() + "\"] | first }}!"
    print(template_str)
    template = environment.from_string(template_str)
    assert template.render(homer=homer) == "Hello, Homer Simpson!"

def test_resource():
    homer = Resource(simpsons.graph, SIM.Homer)
    environment = jinja2.Environment()
    environment.filters["property"] = property
    template_str = "Hello, {{ homer[\"" + FOAF.name.n3() + "\"] | join(', ') }}!"
    template_str = undent("""
        Hello, {{ homer[\"""" + FOAF.name.n3() + """\"] | first }}!

        Don't forget to bring a bouquet for {{ homer[\"""" + FAM.hasSpouse.n3() + """\"] | first | property(\"""" + FOAF.name.n3() +  """\") | first }}.

        Also your kids, {{ homer[\"^""" + FAM.hasFather.n3() + """\"] | first | property(\"""" + FOAF.name.n3() +  """\") | first }} are waiting for dinner.
        """)
    print(template_str)
    template = environment.from_string(template_str)
    assert template.render(homer=homer) == "Hello, Homer Simpson!"
