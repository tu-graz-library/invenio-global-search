# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2025 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""CLI."""

from warnings import warn

from invenio_access.permissions import system_identity
from invenio_records_global_search.records.api import GlobalSearchRecord

from .components import map_metadata_from_a_to_b
from .serializers import (
    LOMRecordJSONSerializer,
    Marc21RecordJSONSerializer,
    RDMRecordJSONSerializer,
)

try:
    from invenio_rdm_records.records.api import RDMRecord

    def rebuild_database_rdm() -> None:
        """Rebuild index rdm."""
        records = RDMRecord.model_cls.query.all()
        for rec in records:
            record = RDMRecord(rec.data, model=rec)
            map_metadata_from_a_to_b(
                record,
                serializer_cls=RDMRecordJSONSerializer,
                schema="rdm",
                identity=system_identity,
            )

    def update_missing_rdm_records() -> None:
        """Update GS with missing rdm records."""
        gs_rdm_records_ids = []
        all_gs_records = GlobalSearchRecord.model_cls.query.all()
        for gs_rec in all_gs_records:
            gs_record = GlobalSearchRecord(gs_rec.data, model=gs_rec)
            if gs_record["original"]["schema"] == "rdm":
                gs_rdm_records_ids.append(gs_record["original"]["pid"])

        records = RDMRecord.model_cls.query.all()
        for rec in records:
            record = RDMRecord(rec.data, model=rec)
            if record["id"] not in gs_rdm_records_ids:
                map_metadata_from_a_to_b(
                    record,
                    serializer_cls=RDMRecordJSONSerializer,
                    schema="rdm",
                    identity=system_identity,
                )

except ImportError:

    def rebuild_database_rdm() -> None:
        """Warn dummy function."""
        msg = "The invenio-rdm-records package is not installed into your system."
        warn(msg, stacklevel=2)

    def update_missing_rdm_records() -> None:
        """Warn dummy function."""
        msg = "The invenio-rdm-records package is not installed into your system."
        warn(msg, stacklevel=2)


try:
    from invenio_records_lom.records.api import LOMRecord
    from invenio_records_lom.utils import LOMMetadata

    def rebuild_database_lom() -> None:
        """Rebuild index lom."""
        records = LOMRecord.model_cls.query.all()
        for rec in records:
            record = LOMRecord(rec.data, model=rec)
            map_metadata_from_a_to_b(
                record,
                serializer_cls=LOMRecordJSONSerializer,
                metadata_cls=LOMMetadata,
                schema="lom",
                identity=system_identity,
            )

    def update_missing_lom_records() -> None:
        """Update GS with missing lom records."""
        gs_lom_records_ids = []
        all_gs_records = GlobalSearchRecord.model_cls.query.all()
        for gs_rec in all_gs_records:
            gs_record = GlobalSearchRecord(gs_rec.data, model=gs_rec)
            if gs_record["original"]["schema"] == "lom":
                gs_lom_records_ids.append(gs_record["original"]["pid"])

        records = LOMRecord.model_cls.query.all()
        for rec in records:
            record = LOMRecord(rec.data, model=rec)
            if record["id"] not in gs_lom_records_ids:
                map_metadata_from_a_to_b(
                    record,
                    serializer_cls=LOMRecordJSONSerializer,
                    metadata_cls=LOMMetadata,
                    schema="lom",
                    identity=system_identity,
                )

except ImportError:

    def rebuild_database_lom() -> None:
        """Warn dummy function."""
        msg = "The invenio-records-lom package is not installed into your system."
        warn(msg, stacklevel=2)

    def update_missing_lom_records() -> None:
        """Warn dummy function."""
        msg = "The invenio-records-lom package is not installed into your system."
        warn(msg, stacklevel=2)


try:
    from invenio_records_marc21.records.api import Marc21Record
    from invenio_records_marc21.services.record import Marc21Metadata

    def rebuild_database_marc21() -> None:
        """Rebuild index marc21."""
        records = Marc21Record.model_cls.query.all()
        for rec in records:
            record = Marc21Record(rec.data, model=rec)
            map_metadata_from_a_to_b(
                record,
                serializer_cls=Marc21RecordJSONSerializer,
                metadata_cls=Marc21Metadata,
                schema="marc21",
                identity=system_identity,
            )

    def update_missing_marc21_records() -> None:
        """Update GS with missing marc21 records."""
        gs_marc21_records_ids = []
        all_gs_records = GlobalSearchRecord.model_cls.query.all()
        for gs_rec in all_gs_records:
            gs_record = GlobalSearchRecord(gs_rec.data, model=gs_rec)
            if gs_record["original"]["schema"] == "marc21":
                gs_marc21_records_ids.append(gs_record["original"]["pid"])

        records = Marc21Record.model_cls.query.all()
        for rec in records:
            record = Marc21Record(rec.data, model=rec)
            if record["id"] not in gs_marc21_records_ids:
                map_metadata_from_a_to_b(
                    record,
                    serializer_cls=Marc21RecordJSONSerializer,
                    metadata_cls=Marc21Metadata,
                    schema="marc21",
                    identity=system_identity,
                )

except ImportError:

    def rebuild_database_marc21() -> None:
        """Warn dummy function."""
        msg = "The invenio-records-marc21 package is not installed into your system."
        warn(msg, stacklevel=2)

    def update_missing_marc21_records() -> None:
        """Warn dummy function."""
        msg = "The invenio-records-marc21 package is not installed into your system."
        warn(msg, stacklevel=2)
