# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Components to Hook into other data models."""

from __future__ import annotations

from collections.abc import Callable

from flask_principal import Identity
from invenio_rdm_records.records.api import RDMDraft, RDMRecord
from invenio_rdm_records.resources.serializers.dublincore import (
    DublinCoreJSONSerializer,
)
from invenio_records_dublin_core import current_records_dublin_core
from invenio_records_resources.services.records.components import ServiceComponent
from invenio_records_resources.services.uow import Operation

from .serializers import LOMRecordJSONSerializer, Marc21RecordJSONSerializer


class ComponentOp(Operation):
    """ComponentOp."""

    def __init__(self, record: RDMRecord, func: Callable) -> None:
        """Construct."""
        self._record = record
        self._func = func

    def on_post_commit(self, uow) -> None:  # noqa: ARG002
        """Post commit."""
        self._func(self._record)


class Marc21ToDublinCoreComponent(ServiceComponent):
    """Marc21ToDublinCoreComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,  # noqa: ARG002
        record: RDMRecord | None = None,
        **_: dict,
    ) -> None:
        """Create handler."""

        def func(record: RDMRecord) -> None:
            record_serializer = Marc21RecordJSONSerializer()
            data = record.dumps()
            metadata = record_serializer.dump_obj(data)
            pid = record["id"]
            original = {
                "view": f"marc21/{pid}",
                "schema": "marc21",
            }
            data = {
                "metadata": metadata,
                "original": original,
            }
            current_records_dublin_core.record_service.create(
                identity=identity,
                data=data,
            )

        self.uow.register(ComponentOp(record, func=func))


class LOMToDublinCoreComponent(ServiceComponent):
    """LOMToDublinCoreComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,  # noqa: ARG002
        record: RDMRecord | None = None,
        **_: dict,
    ) -> None:
        """Create handler."""

        def func(record: RDMRecord) -> None:
            record_serializer = LOMRecordJSONSerializer()
            data = record.dumps()
            metadata = record_serializer.dump_obj(data)
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

        self.uow.register(ComponentOp(record, func=func))


class RDMToDublinCoreComponent(ServiceComponent):
    """RDMToDublinCoreComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,  # noqa: ARG002
        record: RDMRecord | None = None,
        draft: RDMDraft | None = None,
        **_: dict,
    ) -> None:
        """Create handler."""

        def func(record: RDMRecord) -> None:
            record_serializer = DublinCoreJSONSerializer()
            data = record.dumps()
            metadata = record_serializer.dump_obj(data)
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

        if draft["access"]["record"] == "public":
            self.uow.register(ComponentOp(record, func=func))
