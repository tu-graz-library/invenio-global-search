# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2025 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Global Search LOM schema."""

from ..base import NoOpSchema

try:
    from invenio_records_lom.resources.serializers.dublincore.schema import (
        LOMToDublinCoreRecordSchema,
    )
except ImportError:
    LOMToDublinCoreRecordSchema = NoOpSchema


class LOMRecordSchema(LOMToDublinCoreRecordSchema):
    """LOMRecordsSerializer."""
