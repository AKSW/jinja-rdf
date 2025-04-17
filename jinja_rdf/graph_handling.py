"""This module includes methods to handle graphs in the context of static site
generation and templating."""

from urllib.parse import urlsplit, urlunsplit
from rdflib import Graph, URIRef, BNode, IdentifiedNode
from pathlib import Path, PosixPath
from hashlib import md5

from typing import TypeAlias, NamedTuple

"""An IRI either as rdflib URIRef or as a NamedTuple as it is returned by
urllib.parse.urlsplit"""
IRIRef_or_Parts: TypeAlias = (
    URIRef
    | NamedTuple[
        str, str, str, str, str, str | None, str | None, str | None, str | None
    ]
)
Node_or_Parts: TypeAlias = IdentifiedNode | IRIRef_or_Parts


def node_to_path(
    node: Node_or_Parts,
    base_iri: IRIRef_or_Parts,
    base_path: None | Path = None,
    collect_blank: None | Path = None,
    collect_outside: None | Path = None,
) -> tuple[Path | None, str | None]:
    """Convert any identified node to a relative filesystem path.

    If the iri matches the base_iri, it is trimmed.
    If the iri does not match the base_iri resp. is not relative to it, the path
    will represent the complete iri and be put under collect_outside if it is
    specified.
    If the input is a blank node, the path will be relative to collect_blank if
    it is specified.

    Returns: the relative path and an anchor/fragment identifier if the iri
    includes a fragment identifier.
    """
    if not isinstance(node, BNode):
        return iri_to_path(node, base_iri, base_path, collect_outside)
    elif collect_blank:
        return collect_blank / node, None
    return None, None


def iri_to_path(
    iri: IRIRef_or_Parts,
    base_iri: IRIRef_or_Parts,
    base_path: None | Path = None,
    collect_outside: None | Path = None,
) -> tuple[Path | None, str | None]:
    """Convert an IRI to a relative filesystem path.

    If the iri matches the base_iri, it is trimmed.
    If the iri does not match the base_iri resp. is not relative to it, the path
    will represent the complete iri and be put under collect_outside if it is
    specified.
    """
    iri, base_iri = split_iris(iri, base_iri)

    if iri_is_relative_to(iri, base_iri):
        """iri is relative to the base. Just convert the remaining part."""
        resulting_path = PosixPath(iri.path).relative_to(base_iri.path)
        if base_path:
            resulting_path = base_path.joinpath(resulting_path)
        return resulting_path + "?" + iri.query, get_fragment_id(iri)

    if collect_outside:
        """iri is not relative to the base. convert schema, netloc, path and query to a path."""
        resulting_path = PosixPath(f"{iri.schema}_{iri.netloc}") / iri.path
        if base_path:
            resulting_path = base_path.joinpath(resulting_path)
        return resulting_path, get_fragment_id(iri)

    return None, None


def graph_to_paths(graph: Graph, selection: str):
    for row in graph.query(selection):
        row.resourceIri


def get_fragment_id(
    iri: IRIRef_or_Parts,
    base_iri: IRIRef_or_Parts | None = None,
    fallback_generate: bool = False,
) -> str | None:
    """Get the fragement identifier of an IRI or optionally generate an md5 sum
    of the iri to use as an identifier, if none is present.

    base_iri (default: None): Only return the frament identifier, if the iri is
    relative to this base, else fallback to md5 or None. (This can be used to
    only get fragment identifiers for iris on the current page.)
    fallback_generate (default: False): if true it will generate an md5 sum if
    not fragment identifier was found."""
    iri, base_iri = split_iris(iri, base_iri)

    fragment = iri.fragment

    if base_iri and not iri_is_relative_to(iri, base_iri):
        fragment = ""
    if not fragment and fallback_generate:
        return md5(urlunsplit(iri))
    return fragment or None


def iri_is_relative_to(iri: IRIRef_or_Parts, base_iri: IRIRef_or_Parts):
    """Check if an IRI is relative to some base IRI."""
    iri, base_iri = split_iris(iri, base_iri)
    return base_iri[0:1] == iri[0:1] and PosixPath(iri.path).is_relative_to(
        base_iri.path
    )


def split_iris(*args):
    """Takes an arbitrary number of iri arguments either as str/URIRef or
    NamedTuple and return all as NamedTuple as returned by urlsplit."""
    for iri in args:
        if iri and not isinstance(iri, NamedTuple):
            yield urlsplit(iri)
