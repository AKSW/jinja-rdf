from jinja_rdf.rdf_resource import RDFResource as Resource
from jinja_rdf.rdf_property import (
    rdf_property,
    rdf_inverse_property,
    rdf_inverse_properties,
)
from jinja_rdf.sparql_query import sparql_query
from simpsons_rdf import simpsons, SIM, FAM
from rdflib.namespace import FOAF
from undent import undent
import jinja2


def test_resource():
    homer = Resource(simpsons.graph, SIM.Homer)
    environment = jinja2.Environment()
    template_str = 'Hello, {{ homer["' + FOAF.name.n3() + '"] | first }}!'
    print(template_str)
    template = environment.from_string(template_str)
    assert template.render(homer=homer) == "Hello, Homer Simpson!"


def test_resource_property():
    homer = Resource(simpsons.graph, SIM.Homer)
    environment = jinja2.Environment()
    environment.filters["property"] = rdf_property
    template_str = 'Hello, {{ homer | property("' + FOAF.name.n3() + '") }}!'
    print(template_str)
    template = environment.from_string(template_str)
    assert template.render(homer=homer) == "Hello, Homer Simpson!"


def test_resource_registered_namespace():
    homer = Resource(simpsons.graph, SIM.Homer)
    environment = jinja2.Environment()
    template_str = 'Hello, {{ homer["foaf:name"] | first }}!'
    template = environment.from_string(template_str)
    assert template.render(homer=homer) == "Hello, Homer Simpson!"


def test_object_list():
    homer = Resource(simpsons.graph, SIM.Homer)
    environment = jinja2.Environment()
    template_str = 'Hello, {{ homer["' + FOAF.name.n3() + "\"] | join(', ') }}!"
    template = environment.from_string(template_str)
    assert template.render(homer=homer) == "Hello, Homer Simpson!"


def test_chaining_with_property():
    homer = Resource(simpsons.graph, SIM.Homer)
    environment = jinja2.Environment()
    environment.filters["property"] = rdf_property
    environment.filters["inv_property"] = rdf_inverse_property
    template_str = undent(
        """
        Hello, {{ homer[\""""
        + FOAF.name.n3()
        + """\"] | first }}!

        Don't forget to bring a bouquet for {{ homer[\""""
        + FAM.hasSpouse.n3()
        + """\"] | first | property(\""""
        + FOAF.name.n3()
        + """\") }}.
        """
    )
    template = environment.from_string(template_str)
    assert (
        template.render(homer=homer)
        == "Hello, Homer Simpson!\n\nDon't forget to bring a bouquet for Marge Simpson."
    )


def test_chaining_with_resource_item():
    homer = Resource(simpsons.graph, SIM.Homer)
    environment = jinja2.Environment()
    environment.filters["property"] = rdf_property
    template_str = undent(
        """
        Hello, {{ homer[\""""
        + FOAF.name.n3()
        + """\"] | first }}!

        {% set marge = homer[\""""
        + FAM.hasSpouse.n3()
        + """\"] | first -%}
        Don't forget to bring a bouquet for {{ marge["foaf:name"] | first }}.
        """
    )
    template = environment.from_string(template_str)
    assert (
        template.render(homer=homer)
        == "Hello, Homer Simpson!\n\nDon't forget to bring a bouquet for Marge Simpson."
    )


def test_inverse_property():
    homer = Resource(simpsons.graph, SIM.Homer)
    environment = jinja2.Environment()
    environment.filters["property"] = rdf_property
    environment.filters["inv_property"] = rdf_inverse_property
    environment.filters["inv_properties"] = rdf_inverse_properties
    template_str = undent(
        """
        Hello, {{ homer[\""""
        + FOAF.name.n3()
        + """\"] | first }}!

        Don't forget to bring a bouquet for {{ homer[\""""
        + FAM.hasSpouse.n3()
        + """\"] | first | property(\""""
        + FOAF.name.n3()
        + """\") }}.

        Also your kids, {% for kid in homer | inv_properties(\""""
        + FAM.hasFather.n3()
        + """\") %}{% if loop.last %}and {% endif %}{{ kid | property(\""""
        + FOAF.name.n3()
        + """\") }}{% if not loop.last %}, {% endif %}{% endfor %} are waiting for dinner.
        """
    )
    template = environment.from_string(template_str)
    result = template.render(homer=homer)
    assert (
        "Hello, Homer Simpson!\n\nDon't forget to bring a bouquet for Marge Simpson.\n\nAlso your kids, "
        in result
    )
    assert " are waiting for dinner." in result
    assert "Bart Simpson" in result
    assert "Lisa Simpson" in result
    assert "Maggie Simpson" in result


def test_sparql():
    homer = Resource(simpsons.graph, SIM.Homer)
    environment = jinja2.Environment()
    environment.filters["property"] = rdf_property
    environment.filters["inv_properties"] = rdf_inverse_properties
    environment.filters["sparql_query"] = sparql_query

    query = undent("""select ?kid ?name {
        ?kid fam:hasFather ?resourceUri ;
            foaf:name ?name .
    }""")

    template_str = undent(
        """
        Hello, {{ homer[\""""
        + FOAF.name.n3()
        + """\"] | first }}!

        Also your kids, {% for row in homer | sparql_query(\""""
        + query
        + """\") %}{% if loop.last %}and {% endif %}{{ row["name"] }}{% if not loop.last %}, {% endif %}{% endfor %} are waiting for dinner.
        """
    )
    template = environment.from_string(template_str)
    result = template.render(homer=homer)
    assert "Hello, Homer Simpson!" in result
    assert "Also your kids, " in result
    assert " are waiting for dinner." in result
    assert "Bart Simpson" in result
    assert "Lisa Simpson" in result
    assert "Maggie Simpson" in result
