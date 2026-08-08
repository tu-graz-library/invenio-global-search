# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2025 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Serializers."""

from flask_resources import BaseListSchema, MarshmallowSerializer
from flask_resources.serializers import JSONSerializer


def get_last_token_from_path(path: str) -> str:
    """Get last element from a path-like string."""
    tk = path.split("/")[-1]
    return tk[0].upper() + tk[1:]


def split_cc(s: str) -> str:
    """Split CamelCase strings."""
    result = ""
    start = 0
    for i, c in enumerate(s[1:], 1):
        if c.isupper():
            result += s[start:i]
            result += " "
            start = i
    result += s[start:]
    return result


try:
    from invenio_records_lom.resources.serializers.dublincore.schema import (
        LOMToDublinCoreRecordSchema,
    )
    from invenio_records_lom.utils import LOMMetadata

    class GlobalSearchLOMToDublinCoreRecordSchema(LOMToDublinCoreRecordSchema):
        """Override methods from invenio_records_lom LOMToDublinCoreRecordSchema."""

        def get_rights(self, lom: LOMMetadata) -> list:
            """Get rights.

            Method was overriden to take just the name of the right, no need for
            link in global-search context.
            """
            params = ["name"]
            return lom.get_rights(params=params)

    class LOMRecordJSONSerializer(MarshmallowSerializer):
        """Marshmallow based DataCite serializer for records."""

        def __init__(self) -> None:
            """Construct."""
            super().__init__(
                format_serializer_cls=JSONSerializer,
                object_schema_cls=GlobalSearchLOMToDublinCoreRecordSchema,
                list_schema_cls=BaseListSchema,
            )

except ImportError:

    class LOMRecordJSONSerializer(MarshmallowSerializer):
        """Dummy class."""


try:
    from invenio_records_marc21.resources.serializers.dublin_core.schema import (
        DublinCoreSchema as Marc21DublinCoreSchema,
    )

    class Marc21RecordJSONSerializer(MarshmallowSerializer):
        """Marshmallow based DataCite serializer for records."""

        def __init__(self) -> None:
            """Construct."""
            super().__init__(
                format_serializer_cls=JSONSerializer,
                object_schema_cls=Marc21DublinCoreSchema,
                list_schema_cls=BaseListSchema,
            )

except ImportError:

    class Marc21RecordJSONSerializer(MarshmallowSerializer):
        """Dummy class."""


try:
    from invenio_rdm_records.resources.serializers.dublincore.schema import (
        DublinCoreSchema as RDMDublinCoreSchema,
    )
    from marshmallow import missing

    class GlobalSearchRDMDublinCoreSchema(RDMDublinCoreSchema):
        """Override methods from invenio_rdm_records RDMDublinCoreSchema."""

        def get_rights(self, obj: dict) -> list[str]:
            """Get rights."""
            rights = super().get_rights(obj)
            if rights == missing:
                return missing

            gs_rights = []
            for right in rights:
                if "http" in right:
                    # superclass method populates the rights with both links
                    # and right title. for global-search visual context, keep
                    # just the titles
                    continue
                if "access" in right.lower():
                    # here expected "/link/to/<Access_type>Access" string
                    # goal is to have it displayed as "Access_type Access"
                    access = split_cc(get_last_token_from_path(right))
                    gs_rights.append(access)
                else:
                    gs_rights.append(right)

            return gs_rights

        def get_types(self, obj: dict) -> list[str]:
            """Get resource type."""
            orig_types = super().get_types(obj)
            if orig_types == missing:
                return missing

            # expected t to be "link/to/resource_type", goal is to have it
            # displayed as "resource_type"
            return [split_cc(get_last_token_from_path(t)) for t in orig_types]

    class RDMRecordJSONSerializer(MarshmallowSerializer):
        """Marshmallow based DataCite serializer for records."""

        def __init__(self) -> None:
            """Construct."""
            super().__init__(
                format_serializer_cls=JSONSerializer,
                object_schema_cls=GlobalSearchRDMDublinCoreSchema,
                list_schema_cls=BaseListSchema,
            )

except ImportError:

    class RDMRecordJSONSerializer(MarshmallowSerializer):
        """Dummy class."""
