# RDFLib Jinja

This project aims at providing the necessary means to render contents of and RDF Graph with [RDFLib](https://rdflib.readthedocs.io/) in a [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) (jinja2) template.

## Data Model
Provide wrappers around the RDFLib classes to efficiently use the objects in a template.

## Filters
Maybe it is required to also provide specific filters?

## Similar Systems
This library is inspired by [JekyllRDF](https://github.com/AKSW/jekyll-rdf)

### Migrate from JekyllRDF

The scope of JekyllRDF is wider, it covers the representation of an entire graph with multiple templates for classes.
This library just covers individual templates in various contexts.

The Resource class in JekyllRDF has the following attributes:

- `Resource.statements_as_subject`
- `Resource.statements_as_predicate`
- `Resource.statements_as_object`
- `Resource.inspect`

The following attributes are only relevant in the wider JekyllRDF context:
- `Resource.page_url`
- `Resource.render_path`
- `Resource.covered`
- `Resource.rendered`

Those are the filters provided by JekyllRDF.

- `rdf_get`
- `rdf_property`  -> `rdf_property`, `Resource[]`
- `rdf_inverse_property` -> `rdf_inverse_property`
- `sparql_query`  -> `sparql_query` (TODO)
- `rdf_container`
- `rdf_collection`
