# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2025 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Global Search LOM serializer."""

from flask_resources import BaseListSchema
from flask_resources.serializers import JSONSerializer

from ..base import BaseGlobalSearchSerializer, NoOpSchema
from .schema import LOMRecordSchema


class LOMRecordJSONSerializer(BaseGlobalSearchSerializer):
    """Marshmallow based DataCite serializer for records."""

    def __init__(self, **kwargs: dict) -> None:
        """Construct."""
        super().__init__(
            no_op=issubclass(LOMRecordSchema, NoOpSchema),
            format_serializer_cls=JSONSerializer,
            object_schema_cls=LOMRecordSchema,
            list_schema_cls=BaseListSchema,
            **kwargs,
        )
