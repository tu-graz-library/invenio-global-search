# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2025 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Global Search rdm serializer."""

from flask_resources import BaseListSchema
from flask_resources.serializers import JSONSerializer

from .. import BaseGlobalSearchSerializer
from ..base import NoOpSchema
from .schema import RDMRecordSchema


class RDMRecordJSONSerializer(BaseGlobalSearchSerializer):
    """Marshmallow based DataCite serializer for records."""

    def __init__(self, **kwargs: dict) -> None:
        """Construct."""
        super().__init__(
            no_op=issubclass(RDMRecordSchema, NoOpSchema),
            format_serializer_cls=JSONSerializer,
            object_schema_cls=RDMRecordSchema,
            list_schema_cls=BaseListSchema,
            **kwargs,
        )
