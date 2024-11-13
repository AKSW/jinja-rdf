from rdflib.resource import Resource as RDFResource
from rdflib.util import from_n3

class Resource(RDFResource):
    def __getitem__(self, item):
        if isinstance(item, str):
            return self._cast_list(super().__getitem__(from_n3(item)))
        return self._cast_list(super().__getitem__(item))

    def _cast_list(self, list):
        for item in list:
            yield self._cast(item)
