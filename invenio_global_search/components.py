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
from invenio_records_marc21.services.record import Marc21Metadata
from invenio_records_resources.services.records.components import ServiceComponent
from invenio_records_resources.services.uow import Operation

from .serializers import LOMRecordJSONSerializer, Marc21RecordJSONSerializer
from .utils import LOMMetadata


def map_metadata_from_a_to_b(
    record,
    serializer_cls=None,
    metadata_cls=None,
    schema=None,
    identity=None,
) -> None:
    """Func."""
    record_serializer = serializer_cls()
    data = record.dumps()
    obj = metadata_cls(json=data["metadata"]) if metadata_cls else data
    metadata = record_serializer.dump_obj(obj)
    pid = record["id"]
    path = schema if schema != "rdm" else "records"
    original = {
        "view": f"{path}/{pid}",
        "schema": schema,
    }
    data = {
        "metadata": metadata,
        "original": original,
    }
    current_records_dublin_core.records_service.create(
        identity=identity,
        data=data,
    )


class ComponentOp(Operation):
    """ComponentOp."""

    def __init__(
        self,
        record: RDMRecord,
        func: Callable = map_metadata_from_a_to_b,
        serializer_cls=None,
        metadata_cls=None,
        schema=None,
        identity=None,
    ) -> None:
        """Construct."""
        self._record = record
        self._func = func
        self._serializer_cls = serializer_cls
        self._metadata_cls = metadata_cls
        self._schema = schema
        self._identity = identity

    def on_post_commit(self, uow) -> None:  # noqa: ARG002
        """Post commit."""
        self._func(
            self._record,
            self._serializer_cls,
            self._metadata_cls,
            self._schema,
            self._identity,
        )


class Marc21ToDublinCoreComponent(ServiceComponent):
    """Marc21ToDublinCoreComponent."""

    def create(self, identity, data=None, record=None, draft=None, errors=None):
        """Create."""
        print(
            f"components.py create data: {data}, draft: {draft}, record:{record}, errors: {errors}"
        )
        record_serializer = Marc21RecordJSONSerializer()
        marc21 = Marc21Metadata(json=data["metadata"])
        # data = record.dumps()
        metadata = record_serializer.dump_obj(marc21)
        print(f"components.py create metadata: {metadata}")

    def update_draft(self, identity, data=None, record=None, errors=None):
        """Update draft."""
        print(f"components.py update_draft data: {data}")
        record_serializer = Marc21RecordJSONSerializer()
        data = record.dumps()
        marc21 = Marc21Metadata(json=data["metadata"])
        metadata = record_serializer.dump_obj(marc21)
        print(f"components.py update_draft metadata: {metadata}")

    def edit(self, identity, draft=None, record=None):
        """Edit."""
        # print(f"components.py edit draft: {draft}, record: {record}")

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,  # noqa: ARG002
        record: RDMRecord | None = None,
        **_: dict,
    ) -> None:
        """Create handler."""
        cmp_op = ComponentOp(
            record,
            serializer_cls=Marc21RecordJSONSerializer,
            metadata_cls=Marc21Metadata,
            schema="marc21",
            identity=identity,
        )
        self.uow.register(cmp_op)


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
        cmp_op = ComponentOp(
            record,
            serializer_cls=LOMRecordJSONSerializer,
            metadata_cls=LOMMetadata,
            schema="lom",
            identity=identity,
        )
        self.uow.register(cmp_op)


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
        if draft["access"]["record"] != "public":
            return

        cmp_op = ComponentOp(
            record,
            serializer_cls=DublinCoreJSONSerializer,
            schema="rdm",
            identity=identity,
        )
        self.uow.register(cmp_op)
