# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2025 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Components to Hook into other data models."""

from collections.abc import Callable

from flask import current_app
from flask_principal import Identity

try:
    from invenio_rdm_records.records.api import RDMDraft, RDMRecord
except ImportError:
    RDMRecord = type("RDMRecord")
    DublinCoreJSONSerializer = type("DublinCoreJSONSerializer")


from invenio_records.api import Record
from invenio_records_global_search import current_records_global_search

try:
    from invenio_records_lom.records import LOMRecord
    from invenio_records_lom.utils import LOMMetadata
except ImportError:
    LOMRecord = type("LOMRecord")
    LOMMetadata = type("LOMMetadata")


try:
    from invenio_records_marc21.records import Marc21Record
    from invenio_records_marc21.services.record import Marc21Metadata
except ImportError:
    Marc21Record = type("Marc21Record")
    Marc21Metadata = type("Marc21Metadata")


from invenio_records_resources.services.records.components import ServiceComponent
from invenio_records_resources.services.uow import Operation, UnitOfWork
from marshmallow.exceptions import ValidationError

from .serializers import (
    BaseGlobalSearchSerializer,
    LOMRecordJSONSerializer,
    Marc21RecordJSONSerializer,
    RDMRecordJSONSerializer,
)


def map_metadata_from_a_to_b(
    record: Record,
    serializer_cls: type[BaseGlobalSearchSerializer],
    schema: str,
    identity: Identity,
    metadata_cls: type[Marc21Metadata] | type[LOMMetadata] | None = None,
) -> None:
    """Func."""
    schema_mapping = {
        "rdm": "records",
        "lom": "oer",
        "marc21": "publications",
    }

    record_serializer = serializer_cls()

    data = record.dumps()

    if data["access"]["record"] != "public":
        return

    obj = metadata_cls(json=data["metadata"]) if metadata_cls else data
    metadata = record_serializer.dump_obj(obj)
    pid = record["id"]
    path = schema_mapping[schema]
    original = {
        "view": f"{path}/{pid}",
        "schema": schema,
        "pid": pid,
    }
    data = {
        "metadata": metadata,
        "original": original,
    }

    try:
        current_records_global_search.records_service.create_or_update(
            identity=identity,
            data=data,
        )
    except ValidationError as error:
        msg = "GLOBAL SEARCH pid: %s has following validation error: %s"
        current_app.logger.warning(msg, pid, error)


class ComponentOp(Operation):
    """ComponentOp."""

    def __init__(
        self,
        record: Record,
        func: Callable = map_metadata_from_a_to_b,
        serializer_cls: type[BaseGlobalSearchSerializer] | None = None,
        metadata_cls: type[Marc21Metadata] | type[LOMMetadata] | None = None,
        schema: str | None = None,
        identity: Identity = None,
    ) -> None:
        """Construct."""
        self._record = record
        self._func = func
        self._serializer_cls = serializer_cls
        self._metadata_cls = metadata_cls
        self._schema = schema
        self._identity = identity

    def on_post_commit(self, _: UnitOfWork) -> None:
        """Post commit."""
        self._func(
            self._record,
            self._serializer_cls,
            self._schema,
            self._identity,
            self._metadata_cls,
        )


class Marc21ToGlobalSearchComponent(ServiceComponent):
    """Marc21ToGlobalSearchComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,  # noqa: ARG002
        record: Marc21Record | None = None,
        **__: dict,
    ) -> None:
        """Create handler."""
        cmp_op = ComponentOp(
            record,
            serializer_cls=Marc21RecordJSONSerializer,
            schema="marc21",
            identity=identity,
            metadata_cls=Marc21Metadata,
        )
        self.uow.register(cmp_op)


class LOMToGlobalSearchComponent(ServiceComponent):
    """LOMToGlobalSearchComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,  # noqa: ARG002
        record: LOMRecord | None = None,
        **__: dict,
    ) -> None:
        """Create handler."""
        cmp_op = ComponentOp(
            record,
            serializer_cls=LOMRecordJSONSerializer,
            schema="lom",
            identity=identity,
            metadata_cls=LOMMetadata,
        )
        self.uow.register(cmp_op)


class RDMToGlobalSearchComponent(ServiceComponent):
    """RDMToGlobalSearchComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,  # noqa: ARG002
        record: RDMRecord | None = None,
        draft: RDMDraft | None = None,  # noqa: ARG002
        **__: dict,
    ) -> None:
        """Create handler."""
        cmp_op = ComponentOp(
            record,
            serializer_cls=RDMRecordJSONSerializer,
            schema="rdm",
            identity=identity,
        )
        self.uow.register(cmp_op)
