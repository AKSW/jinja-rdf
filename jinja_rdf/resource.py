from rdflib.resource import Resource as RDFLibResource
from rdflib.util import from_n3

class Resource(RDFLibResource):
    def __getitem__(self, item):
        if isinstance(item, str):
            return super().__getitem__(from_n3(item))
        return super().__getitem__(item)
