from rdflib.resource import Resource as RDFLibResource
from rdflib.util import from_n3
from rdflib.paths import Path
from rdflib.term import (
    Node,
)
from rdflib import BNode, URIRef

class RDFResource(RDFLibResource):
    def __getitem__(self, item):
        if isinstance(item, str) and not isinstance(item, URIRef):
            item = from_n3(item)
        return super().__getitem__(item)

    def _cast(self, node):
        if isinstance(node, (BNode, URIRef)):
            return self._new(node)
        elif isinstance(node, (RDFLibResource)):
            return self._new(node.identifier)
        else:
            return node
