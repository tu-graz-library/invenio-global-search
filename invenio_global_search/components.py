# SPDX-FileCopyrightText: 2023-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Components to Hook into other data models."""

from collections.abc import Callable
from typing import TypeAlias

from flask import current_app
from flask_principal import Identity
from invenio_records.api import Record
from invenio_records_global_search import current_records_global_search
from invenio_records_resources.services.base.config import ConfiguratorMixin
from invenio_records_resources.services.records.components import ServiceComponent
from invenio_records_resources.services.uow import Operation, UnitOfWork
from marshmallow.exceptions import ValidationError

from .serializers import (
    LOMRecordJSONSerializer,
    Marc21RecordJSONSerializer,
    RDMRecordJSONSerializer,
)

GlobalSearchSerializerType: TypeAlias = (
    type[LOMRecordJSONSerializer]
    | type[Marc21RecordJSONSerializer]
    | type[RDMRecordJSONSerializer]
)


try:
    from invenio_rdm_records.records.api import RDMDraft, RDMRecord
    from invenio_rdm_records.services.config import RDMRecordServiceConfig

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

except ImportError:

    class RDMToGlobalSearchComponent(ServiceComponent):  # type: ignore[no-redef]
        """RDMToGlobalSearchComponent."""

    class RDMRecordServiceConfig(ConfiguratorMixin):  # type: ignore[no-redef]
        """Dummy."""


try:
    from invenio_records_lom.records import LOMRecord
    from invenio_records_lom.services.config import LOMRecordServiceConfig
    from invenio_records_lom.utils import LOMMetadata

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

except ImportError:

    class LOMMetadata:  # type: ignore[no-redef]
        """Dummy class to have it for type checker."""

    class LOMToGlobalSearchComponent(ServiceComponent):  # type: ignore[no-redef]
        """Dummy class."""

    class LOMRecordServiceConfig(ConfiguratorMixin):  # type: ignore[no-redef]
        """Dummy."""


try:
    from invenio_records_marc21.records import Marc21Record
    from invenio_records_marc21.services.config import Marc21RecordServiceConfig
    from invenio_records_marc21.services.record import Marc21Metadata

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

except ImportError:

    class Marc21Metadata:  # type: ignore[no-redef]
        """Dummy class to have it for type checker."""

    class Marc21ToGlobalSearchComponent(ServiceComponent):  # type: ignore[no-redef]
        """Marc21ToGlobalSearchComponent."""

    class Marc21RecordServiceConfig(ConfiguratorMixin):  # type: ignore[no-redef]
        """Dummy."""


def map_metadata_from_a_to_b(
    record: Record,
    serializer_cls: GlobalSearchSerializerType,
    schema: str,
    identity: Identity,
    metadata_cls: type[Marc21Metadata] | type[LOMMetadata] | None = None,
) -> None:
    """Func."""
    schema_mapping = {
        "rdm": RDMRecordServiceConfig,
        "lom": LOMRecordServiceConfig,
        "marc21": Marc21RecordServiceConfig,
    }

    record_serializer = serializer_cls()

    data = record.dumps()

    if data["access"]["record"] != "public":
        return

    obj = (
        metadata_cls(json=data["metadata"])  # ty: ignore[unknown-argument]
        if metadata_cls
        else data
    )
    pid = record["id"]
    try:
        metadata = record_serializer.dump_obj(obj)
    except Exception:
        msg = "Record pid: %s with schema %s has a serialization error."
        current_app.logger.exception(msg, pid, schema)
        return

    service_config = schema_mapping[schema].build(current_app)
    link = service_config.links_item["self_html"].expand(record, {})

    original = {
        "view": link,
        "schema": schema,
        "pid": pid,
        "created": data["created"],
        "access": {
            "status": data["access"]["status"],
        },
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

    def __init__(  # noqa: PLR0917
        self,
        record: Record,
        serializer_cls: GlobalSearchSerializerType,
        func: Callable = map_metadata_from_a_to_b,
        metadata_cls: type[Marc21Metadata] | type[LOMMetadata] | None = None,
        schema: str | None = None,
        identity: Identity | None = None,
    ) -> None:
        """Construct."""
        self._record = record
        self._func = func
        self._serializer_cls = serializer_cls
        self._metadata_cls = metadata_cls
        self._schema = schema
        self._identity = identity

    def on_post_commit(  # ty: ignore[invalid-method-override]
        self,
        _: UnitOfWork,
    ) -> None:
        """Post commit."""
        self._func(
            self._record,
            self._serializer_cls,
            self._schema,
            self._identity,
            self._metadata_cls,
        )
