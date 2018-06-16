# -*- coding: utf-8 -*-

from haystack.backends.whoosh_backend import WhooshEngine, WhooshSearchBackend
from whoosh.analysis import CharsetFilter, StemmingAnalyzer, NgramFilter
from whoosh.support.charset import accent_map
from whoosh.fields import TEXT, NGRAM, NGRAMWORDS


class FoldingWhooshSearchBackend(WhooshSearchBackend):

    def build_schema(self, fields):
        schema = super(FoldingWhooshSearchBackend, self).build_schema(fields)

        for name, field in schema[1].items():
            if isinstance(field, TEXT) or isinstance(field, NGRAM) or isinstance(field, NGRAMWORDS):
                field.analyzer = StemmingAnalyzer() | CharsetFilter(accent_map) | NgramFilter(minsize=2, maxsize=15)

        return schema


class FoldingWhooshEngine(WhooshEngine):
    backend = FoldingWhooshSearchBackend
