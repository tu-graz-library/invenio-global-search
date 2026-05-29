# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2025 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""CLI."""

from warnings import warn

from invenio_access.permissions import system_identity
from invenio_drafts_resources.records import Record
from invenio_records_global_search.records.api import GlobalSearchRecord

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
    metadata_cls: type | None = None,
) -> None:
    records = record_model_cls.model_cls.query.all()  # ty: ignore[unresolved-attribute]
    for rec in records:
        record = record_model_cls(rec.data, model=rec)
        map_metadata_from_a_to_b(
            record,
            serializer_cls=serializer,
            metadata_cls=metadata_cls,
            schema=schema,
            identity=system_identity,
        )


def _base_update_missing_fn(
    record_model_cls: type[Record],
    serializer: GlobalSearchSerializerType,
    schema: str,
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
        if (
            record["id"] not in gs_rdm_records_ids
            and record["access"]["record"] == "public"
            and "tombstone" not in record
        ):
            map_metadata_from_a_to_b(
                record,
                serializer_cls=serializer,
                metadata_cls=metadata_cls,
                schema=schema,
                identity=system_identity,
            )


try:
    from invenio_rdm_records.records.api import RDMRecord

    def rebuild_database_rdm() -> None:
        """Rebuild index rdm."""
        _base_rebuild_database_fn(RDMRecord, RDMRecordJSONSerializer, "rdm")

    def update_missing_rdm() -> None:
        """Update GS with missing rdm records."""
        _base_update_missing_fn(RDMRecord, RDMRecordJSONSerializer, "rdm")

except ImportError:

    def rebuild_database_rdm() -> None:
        """Warn dummy function."""
        msg = "The invenio-rdm-records package is not installed into your system."
        warn(msg, stacklevel=2)

    def update_missing_rdm() -> None:
        """Warn dummy function."""
        msg = "The invenio-rdm-records package is not installed into your system."
        warn(msg, stacklevel=2)


try:
    from invenio_records_lom.records.api import LOMRecord
    from invenio_records_lom.utils import LOMMetadata

    def rebuild_database_lom() -> None:
        """Rebuild index lom."""
        _base_rebuild_database_fn(
            LOMRecord,
            LOMRecordJSONSerializer,
            "lom",
            metadata_cls=LOMMetadata,
        )

    def update_missing_lom() -> None:
        """Update GS with missing lom records."""
        _base_update_missing_fn(
            LOMRecord,
            LOMRecordJSONSerializer,
            "lom",
            metadata_cls=LOMMetadata,
        )

except ImportError:

    def rebuild_database_lom() -> None:
        """Warn dummy function."""
        msg = "The invenio-records-lom package is not installed into your system."
        warn(msg, stacklevel=2)

    def update_missing_lom() -> None:
        """Warn dummy function."""
        msg = "The invenio-records-lom package is not installed into your system."
        warn(msg, stacklevel=2)


try:
    from invenio_records_marc21.records.api import Marc21Record
    from invenio_records_marc21.services.record import Marc21Metadata

    def rebuild_database_marc21() -> None:
        """Rebuild index marc21."""
        _base_rebuild_database_fn(
            Marc21Record,
            Marc21RecordJSONSerializer,
            "marc21",
            metadata_cls=Marc21Metadata,
        )

    def update_missing_marc21() -> None:
        """Update GS with missing marc21 records."""
        _base_update_missing_fn(
            Marc21Record,
            Marc21RecordJSONSerializer,
            "marc21",
            metadata_cls=Marc21Metadata,
        )

except ImportError:

    def rebuild_database_marc21() -> None:
        """Warn dummy function."""
        msg = "The invenio-records-marc21 package is not installed into your system."
        warn(msg, stacklevel=2)

    def update_missing_marc21() -> None:
        """Warn dummy function."""
        msg = "The invenio-records-marc21 package is not installed into your system."
        warn(msg, stacklevel=2)
