# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2025 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Serializers."""

from flask_resources import BaseListSchema, MarshmallowSerializer
from flask_resources.serializers import JSONSerializer

try:
    from invenio_records_lom.resources.serializers.dublincore.schema import (
        LOMToDublinCoreRecordSchema,
    )

    class LOMRecordJSONSerializer(MarshmallowSerializer):
        """Marshmallow based DataCite serializer for records."""

        def __init__(self) -> None:
            """Construct."""
            super().__init__(
                format_serializer_cls=JSONSerializer,
                object_schema_cls=LOMToDublinCoreRecordSchema,
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

    class RDMRecordJSONSerializer(MarshmallowSerializer):
        """Marshmallow based DataCite serializer for records."""

        def __init__(self) -> None:
            """Construct."""
            super().__init__(
                format_serializer_cls=JSONSerializer,
                object_schema_cls=RDMDublinCoreSchema,
                list_schema_cls=BaseListSchema,
            )

except ImportError:

    class RDMRecordJSONSerializer(MarshmallowSerializer):
        """Dummy class."""
