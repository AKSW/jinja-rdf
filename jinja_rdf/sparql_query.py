from rdflib.resource import Resource as RDFLibResource


def sparql_query(resource: RDFLibResource, query: str):
    return resource.graph.query(
        query, initBindings={"resourceUri": resource.identifier}
    )
