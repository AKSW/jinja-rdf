from .rdf_property import (
    rdf_properties,
    rdf_inverse_properties,
    rdf_property,
    rdf_inverse_property,
)
from .sparql_query import sparql_query


def register_filters(environment):
    """Register all jinja-rdf filters on a jinja environment."""
    environment.filters["properties"] = rdf_properties
    environment.filters["properties_inv"] = rdf_inverse_properties
    environment.filters["property"] = rdf_property
    environment.filters["property_inv"] = rdf_inverse_property
    environment.filters["query"] = sparql_query
