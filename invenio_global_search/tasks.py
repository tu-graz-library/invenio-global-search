# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2026 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Tasks."""

from warnings import warn

from celery import shared_task
from invenio_access.permissions import system_identity
from invenio_drafts_resources.records import Record
from invenio_records_global_search.records.api import GlobalSearchRecord
from invenio_records_resources.services import RecordService

from .components import GlobalSearchSerializerType, map_metadata_from_a_to_b
from .serializers import (
    LOMRecordJSONSerializer,
    Marc21RecordJSONSerializer,
    RDMRecordJSONSerializer,
)


def _base_rebuild_database_fn(
    record_model_cls: type[Record],
    serializer: GlobalSearchSerializerType,
    schema: str,
    records_service: RecordService,
    metadata_cls: type | None = None,
) -> None:
    records = record_model_cls.model_cls.query.all()  # ty: ignore[unresolved-attribute]
    for rec in records:
        record = record_model_cls(rec.data, model=rec)
        try:
            record_item = records_service.read(system_identity, record["id"])
        except Exception as e:  # noqa: BLE001
            warn(f"Exception caught for record {record["id"]}: {e}", stacklevel=2)
            continue
        map_metadata_from_a_to_b(
            record_item._record,  # noqa: SLF001
            serializer_cls=serializer,
            metadata_cls=metadata_cls,
            schema=schema,
            identity=system_identity,
        )


def _base_update_missing_fn(
    record_model_cls: type[Record],
    serializer: GlobalSearchSerializerType,
    schema: str,
    records_service: RecordService,
    metadata_cls: type | None = None,
) -> None:
    gs_rdm_records_ids = []
    all_gs_records = GlobalSearchRecord.model_cls.query.all()
    for gs_rec in all_gs_records:
        gs_record = GlobalSearchRecord(gs_rec.data, model=gs_rec)
        if gs_record["original"]["schema"] == schema:
            gs_rdm_records_ids.append(gs_record["original"]["pid"])

    records = record_model_cls.model_cls.query.all()  # ty: ignore[unresolved-attribute]
    for rec in records:
        record = record_model_cls(rec.data, model=rec)
        try:
            record_item = records_service.read(system_identity, record["id"])
        except Exception as e:  # noqa: BLE001
            warn(f"Exception caught for record {record["id"]}: {e}", stacklevel=2)
            continue

        if record["id"] not in gs_rdm_records_ids:
            map_metadata_from_a_to_b(
                record_item._record,  # noqa: SLF001
                serializer_cls=serializer,
                metadata_cls=metadata_cls,
                schema=schema,
                identity=system_identity,
            )


try:
    from invenio_rdm_records.proxies import current_rdm_records_service
    from invenio_rdm_records.records.api import RDMRecord

    @shared_task
    def rebuild_database_rdm() -> None:
        """Rebuild index rdm."""
        _base_rebuild_database_fn(
            RDMRecord,
            RDMRecordJSONSerializer,
            "rdm",
            current_rdm_records_service,
        )

    @shared_task
    def update_missing_rdm() -> None:
        """Update GS with missing rdm records."""
        _base_update_missing_fn(
            RDMRecord,
            RDMRecordJSONSerializer,
            "rdm",
            current_rdm_records_service,
        )

except ImportError:

    @shared_task
    def rebuild_database_rdm() -> None:
        """Warn dummy function."""
        msg = "The invenio-rdm-records package is not installed into your system."
        warn(msg, stacklevel=2)

    @shared_task
    def update_missing_rdm() -> None:
        """Warn dummy function."""
        msg = "The invenio-rdm-records package is not installed into your system."
        warn(msg, stacklevel=2)


try:
    from invenio_records_lom.proxies import current_records_lom
    from invenio_records_lom.records.api import LOMRecord
    from invenio_records_lom.utils import LOMMetadata

    @shared_task
    def rebuild_database_lom() -> None:
        """Rebuild index lom."""
        _base_rebuild_database_fn(
            LOMRecord,
            LOMRecordJSONSerializer,
            "lom",
            current_records_lom.records_service,
            metadata_cls=LOMMetadata,
        )

    @shared_task
    def update_missing_lom() -> None:
        """Update GS with missing lom records."""
        _base_update_missing_fn(
            LOMRecord,
            LOMRecordJSONSerializer,
            "lom",
            current_records_lom.records_service,
            metadata_cls=LOMMetadata,
        )

except ImportError:

    @shared_task
    def rebuild_database_lom() -> None:
        """Warn dummy function."""
        msg = "The invenio-records-lom package is not installed into your system."
        warn(msg, stacklevel=2)

    @shared_task
    def update_missing_lom() -> None:
        """Warn dummy function."""
        msg = "The invenio-records-lom package is not installed into your system."
        warn(msg, stacklevel=2)


try:
    from invenio_records_marc21.proxies import current_records_marc21
    from invenio_records_marc21.records.api import Marc21Record
    from invenio_records_marc21.services.record import Marc21Metadata

    @shared_task
    def rebuild_database_marc21() -> None:
        """Rebuild index marc21."""
        _base_rebuild_database_fn(
            Marc21Record,
            Marc21RecordJSONSerializer,
            "marc21",
            current_records_marc21.records_service,
            metadata_cls=Marc21Metadata,
        )

    @shared_task
    def update_missing_marc21() -> None:
        """Update GS with missing marc21 records."""
        _base_update_missing_fn(
            Marc21Record,
            Marc21RecordJSONSerializer,
            "marc21",
            current_records_marc21.records_service,
            metadata_cls=Marc21Metadata,
        )

except ImportError:

    @shared_task
    def rebuild_database_marc21() -> None:
        """Warn dummy function."""
        msg = "The invenio-records-marc21 package is not installed into your system."
        warn(msg, stacklevel=2)

    @shared_task
    def update_missing_marc21() -> None:
        """Warn dummy function."""
        msg = "The invenio-records-marc21 package is not installed into your system."
        warn(msg, stacklevel=2)
