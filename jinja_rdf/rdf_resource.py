from rdflib.resource import Resource as RDFLibResource
from rdflib.util import from_n3
from rdflib.paths import Path
from rdflib.term import (
    Node,
)

_PredicateType = Node


class RDFResource(RDFLibResource):
    def __getitem__(self, item):
        if isinstance(item, str):
            return self._cast_list(super().__getitem__(from_n3(item)))
        return self._cast_list(super().__getitem__(item))

    def subjects(self, predicate: None | Path | _PredicateType | str = None):
        if isinstance(predicate, str):
            predicate = from_n3(predicate)
        return self._resources(self._graph.subjects(predicate, self._identifier))

    def _cast_list(self, list):
        for item in list:
            yield self._cast(item)
