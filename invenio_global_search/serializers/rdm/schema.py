# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Global Search rdm schema."""

from flask_resources.serializers import BaseSerializerSchema
from marshmallow import fields


class RDMRecordSchema(BaseSerializerSchema):
    """RDMRecordsSerializer."""

    # contributor = fields.Method("get_contributor")
    title = fields.Method("get_title")
    creator = fields.Method("get_creator")
    identifier = fields.Method("get_identifier")
    # relation = fields.Method("get_relation")
    right = fields.Method("get_right")
    # date = fields.Method("get_date")
    # subject = fields.Method("get_subject")
    # description = fields.Method("get_description")
    # publisher = fields.Method("get_publisher")
    # type = fields.Method("get_type")
    # source = fields.Method("get_source")
    # language = fields.Method("get_language")
    # location = fields.Method("get_location")
    # format = fields.Method("get_format")

    def get_contributor(self, obj: dict) -> str:
        """Get contributors."""
        return ""

    def get_title(self, obj: dict) -> str:
        """Get titles."""
        return obj["metadata"]["title"]

    def get_creator(self, obj: dict) -> str:
        """Get creators."""
        return obj["metadata"]["creators"][0]["person_or_org"]["name"]

    def get_identifier(self, obj: dict) -> str:
        """Get identifiers."""
        # TODO:
        # generate DOI, the problem is that the doi does no exists at this point
        return "DOI"

    def get_relation(self, obj: dict) -> str:
        """Get relations."""
        return ""

    def get_right(self, obj: dict) -> str:
        """Get rights."""
        return obj["metadata"]["rights"][0]["id"]

    def get_date(self, obj: dict) -> str:
        """Get dates."""
        return ""

    def get_subject(self, obj: dict) -> str:
        """Get subjects."""
        return ""

    def get_description(self, obj: dict) -> str:
        """Get descriptions."""
        return ""

    def get_publisher(self, obj: dict) -> str:
        """Get publishers."""
        return ""

    def get_type(self, obj: dict) -> str:
        """Get types."""
        return ""

    def get_source(self, obj: dict) -> str:
        """Get soruces."""
        return ""

    def get_language(self, obj: dict) -> str:
        """Get languages."""
        return ""

    def get_location(self, obj: dict) -> str:
        """Get locations."""
        return ""

    def get_format(self, obj: dict) -> str:
        """Get formats."""
        return ""
