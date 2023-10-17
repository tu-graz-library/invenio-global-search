# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Global Search LOM schema."""

from flask_resources.serializers import BaseSerializerSchema
from marshmallow import fields

from ...utils import LOMMetadata


def get_text(obj: dict) -> str:
    """Get text from langstring."""
    return obj["langstring"]["#text"]


class LOMRecordSchema(BaseSerializerSchema):
    """RDMRecordsSerializer."""

    contributors = fields.Method("get_contributors")
    titles = fields.Method("get_titles")
    creators = fields.Method("get_creators")
    identifiers = fields.Method("get_identifiers")
    relations = fields.Method("get_relations")
    rights = fields.Method("get_rights")
    dates = fields.Method("get_dates")
    subjects = fields.Method("get_subjects")
    descriptions = fields.Method("get_descriptions")
    publishers = fields.Method("get_publishers")
    types = fields.Method("get_types")
    sources = fields.Method("get_sources")
    languages = fields.Method("get_languages")
    locations = fields.Method("get_locations")
    formats = fields.Method("get_formats")

    def get_contributors(self, lom: LOMMetadata) -> list:
        """Get contributors."""
        contributors = []
        for contribute in lom["lifecycle.contribute"]:
            if "entity" in contribute:
                contributors += contribute["entity"]
        return contributors

    def get_titles(self, lom: LOMMetadata) -> list:
        """Get titles."""
        return [lom["general.title.langstring.#text"]]

    def get_creators(self, lom: LOMMetadata) -> list:
        """Get creators."""
        creators = []
        for contribute in lom["lifecycle.contribute"]:
            if "entity" in contribute:
                creators += contribute["entity"]
        return creators

    def get_identifiers(self, lom: LOMMetadata) -> list:
        """Get identifiers."""
        return [get_text(entry["entry"]) for entry in lom["general.identifier"]]

    def get_relations(self, lom: LOMMetadata) -> list:
        """Get relations."""
        relations = []
        for relation in lom["relation"]:
            if "resource" in relation and "description" in relation["resource"]:
                relations += [get_text(relation["resource"]["description"][0])]
        return relations

    def get_rights(self, lom: LOMMetadata) -> list:
        """Get rights."""
        return [lom["rights.url"]]

    def get_dates(self, lom: LOMMetadata) -> list:
        """Get dates."""
        dates = []
        for contribute in lom["lifecycle.contribute"]:
            if "date" in contribute and "datetime" in contribute["date"]:
                dates += [contribute["date"]["datetime"]]
        return dates

    def get_subjects(self, lom: LOMMetadata) -> list:
        """Get subjects."""
        return [get_text(subject) for subject in lom["general.keyword"]]

    def get_descriptions(self, lom: LOMMetadata) -> list:
        """Get descriptions."""
        return [get_text(desc) for desc in lom["general.description"]]

    def get_publishers(self, lom: LOMMetadata) -> list:
        """Get publishers."""
        publishers = []
        for contribute in lom["lifecycle.contribute"]:
            publishers += contribute["entity"]
        return publishers

    def get_types(self, lom: LOMMetadata) -> list:
        """Get types."""
        entry = lom["educational.learningresourcetype.entry"]
        if entry:
            return [get_text(entry)]
        return []

    def get_sources(self, lom: LOMMetadata) -> list:
        """Get soruces."""
        return []

    def get_languages(self, lom: LOMMetadata) -> list:
        """Get languages."""
        languages = lom["general.language"]
        if languages and len(languages) > 0:
            return languages
        return []

    def get_locations(self, lom: LOMMetadata) -> list:
        """Get locations."""
        return []

    def get_formats(self, lom: LOMMetadata) -> list:
        """Get formats."""
        formats = lom["technical.format"]
        if formats and len(formats) > 0:
            return formats
        return []
