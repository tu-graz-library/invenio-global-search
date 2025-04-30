# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2025 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Global Search Marc21 serializer."""

from flask_resources import BaseListSchema
from flask_resources.serializers import JSONSerializer

from ..base import BaseGlobalSearchSerializer, NoOpSchema
from .schema import Marc21RecordSchema


class Marc21RecordJSONSerializer(BaseGlobalSearchSerializer):
    """Marshmallow based DataCite serializer for records."""

    def __init__(self, **kwargs: dict) -> None:
        """Construct."""
        super().__init__(
            no_op=issubclass(Marc21RecordSchema, NoOpSchema),
            format_serializer_cls=JSONSerializer,
            object_schema_cls=Marc21RecordSchema,
            list_schema_cls=BaseListSchema,
            **kwargs,
        )
