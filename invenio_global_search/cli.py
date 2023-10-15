# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""CLI."""

from click import group
from flask.cli import with_appcontext
from invenio_access.permissions import system_identity
from invenio_rdm_records.records.api import RDMRecord
from invenio_rdm_records.resources.serializers.dublincore import (
    DublinCoreJSONSerializer,
)
from invenio_records_lom.records.api import LOMRecord
from invenio_records_marc21.records.api import Marc21Record
from invenio_records_marc21.services.record import Marc21Metadata

from .components import map_metadata_from_a_to_b
from .serializers import LOMRecordJSONSerializer, Marc21RecordJSONSerializer
from .utils import LOMMetadata


def rebuild_database_rdm() -> None:
    """Rebuild index rdm."""
    print("rebuild_database_rdm")
    records = RDMRecord.model_cls.query.all()
    for rec in records:
        record = RDMRecord(rec.data, model=rec)
        map_metadata_from_a_to_b(
            record,
            serializer_cls=DublinCoreJSONSerializer,
            schema="rdm",
            identity=system_identity,
        )


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


@group()
def global_search() -> None:
    """CLI-Group for invenio global search commands."""


@global_search.command()
@with_appcontext
def rebuild_database() -> None:
    """Rebuild all records in database."""
    rebuild_database_marc21()
    rebuild_database_lom()
    rebuild_database_rdm()
