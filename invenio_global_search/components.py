# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Components to Hook into other data models."""

from __future__ import annotations

from flask_principal import Identity
from invenio_records_dublin_core import DublinCoreRecord, current_records_dublin_core
from invenio_records_resources.services.records.components import ServiceComponent

from .serializers import (
    LOMRecordJSONSerializer,
    Marc21RecordJSONSerializer,
    RDMRecordJSONSerializer,
)


class Marc21ToDublinCoreComponent(ServiceComponent):
    """Marc21ToDublinCoreComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,
        record: DublinCoreRecord | None = None,
        **kwargs: dict,
    ) -> None:
        """Create handler."""
        record_serializer = Marc21RecordJSONSerializer()
        metadata = record_serializer.dump_obj(record.metadata)
        data = {"metadata": metadata}
        current_records_dublin_core.record_service.create(
            identity=identity,
            data=data,
        )


class LOMToDublinCoreComponent(ServiceComponent):
    """LOMToDublinCoreComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,
        record: DublinCoreRecord | None = None,
        **kwargs: dict,
    ) -> None:
        """Create handler."""
        record_serializer = LOMRecordJSONSerializer()
        metadata = record_serializer.dump_obj(record)
        pid = record["id"]
        original = {
            "view": f"lom/{pid}",
            "schema": "lom",
        }
        data = {
            "metadata": metadata,
            "original": original,
        }
        current_records_dublin_core.record_service.create(
            identity=identity,
            data=data,
        )


class RDMToDublinCoreComponent(ServiceComponent):
    """RDMToDublinCoreComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,
        record: DublinCoreRecord | None = None,
        **kwargs: dict,
    ) -> None:
        """Create handler."""
        record_serializer = RDMRecordJSONSerializer()
        print(f"RDMToDublinCoreComponent.publish record: {record}")
        metadata = record_serializer.dump_obj(record)
        pid = record["id"]
        original = {
            "view": f"records/{pid}",
            "schema": "rdm",
        }
        data = {
            "metadata": metadata,
            "original": original,
        }
        current_records_dublin_core.record_service.create(
            identity=identity,
            data=data,
        )
