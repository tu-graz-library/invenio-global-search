# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-records-dublin-core is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 schema."""

from marshmallow import Schema, fields

# maybe move that to marc21 from the beginning!


class Contributors(fields.Field):
    """Contributors."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialize."""


class Title(fields.Field):
    """Title."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialize."""


class Marc21Schema(Schema):
    """Marc21 schema."""

    # contributor = Contributors(attribute="metadata.fields")
    # coverage = Coverage()
    # # creator not used
    # date = Date()
    # description = Description()
    # format = Format()
    # identifier = Identifier()
    # language = Language()
    # publisher = Publisher()
    # relation = Relation()
    # rights = Rights()
    # source = Source()
    # subject = Subject()
    title = Title(attribute="metadata.fields")
