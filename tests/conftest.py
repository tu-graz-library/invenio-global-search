# SPDX-FileCopyrightText: 2023-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Pytest configuration."""

from collections.abc import Callable
from typing import Any

import pytest
from flask import Flask
from invenio_app.factory import create_api
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from invenio_records.api import Record
from invenio_records_lom.utils import LOMMetadata
from invenio_records_marc21.services.record import Marc21Metadata

from invenio_global_search.components import GlobalSearchSerializerType
from invenio_global_search.serializers import (
    LOMRecordJSONSerializer,
    Marc21RecordJSONSerializer,
    RDMRecordJSONSerializer,
)

type SchemaConfig = tuple[
    str,
    GlobalSearchSerializerType,
    type[LOMMetadata | Marc21Metadata] | None,
]


class TestRecord(Record):
    """Mock record properties."""

    @property
    def is_draft(self) -> bool:
        """Is draft."""
        return False

    @property
    def is_published(self) -> bool:
        """Is published."""
        return True


RDM_RECORD_DATA: dict[str, Any] = {"title": "test title"}

LOM_RECORD_DATA: dict[str, Any] = {
    "general": {"title": {"langstring": {"#text": "Test", "lang": "en"}}},
}

MARC21_RECORD_DATA: dict[str, Any] = {
    "leader": "00000nam a2200000zca4500",
    "fields": {
        "245": [
            {
                "ind1": "1",
                "ind2": "0",
                "subfields": {"a": ["nulla sunt laborum"]},
            },
        ],
    },
}

RECORD_DATA_BY_SCHEMA: dict[str, dict[str, Any]] = {
    "rdm": RDM_RECORD_DATA,
    "lom": LOM_RECORD_DATA,
    "marc21": MARC21_RECORD_DATA,
}


@pytest.fixture(scope="module")
def create_app() -> Callable[..., Flask]:
    """Create app."""
    return create_api


@pytest.fixture(
    params=[
        (
            "rdm",
            RDMRecordJSONSerializer,
            None,
        ),
        (
            "lom",
            LOMRecordJSONSerializer,
            LOMMetadata,
        ),
        (
            "marc21",
            Marc21RecordJSONSerializer,
            Marc21Metadata,
        ),
    ],
    ids=["rdm", "lom", "marc21"],
)
def schema_configuration(request: pytest.FixtureRequest) -> SchemaConfig:
    """Global search supported data models."""
    return request.param


@pytest.fixture
def record_data(schema_configuration: SchemaConfig) -> dict[str, Any]:
    """Return record data for corresponding schema."""
    schema, _, _ = schema_configuration
    return RECORD_DATA_BY_SCHEMA[schema]


def _build_record(
    record_data: dict[str, Any],
    access: dict[str, str],
) -> TestRecord:
    """Build record."""
    pid = PersistentIdentifier(
        pid_type="recid",
        pid_value="test-record-123",
        status=PIDStatus.REGISTERED,
    )

    data: dict[str, Any] = {
        "id": "test-record-123",
        "created": "2026-01-01T10:00:00",
        "access": access,
        "metadata": record_data,
    }

    rec = TestRecord(data)
    rec.pid = pid  # ty: ignore[missing-attribute]
    return rec


@pytest.fixture
def public_record(record_data: dict[str, Any]) -> TestRecord:
    """Build public access record."""
    return _build_record(
        record_data,
        {
            "record": "public",
            "files": "public",
            "status": "open",
        },
    )


@pytest.fixture
def restricted_record(record_data: dict[str, Any]) -> TestRecord:
    """Build fully restricted record."""
    return _build_record(
        record_data,
        {
            "record": "restricted",
            "files": "restricted",
            "status": "restricted",
        },
    )


@pytest.fixture
def restricted_files_record(record_data: dict[str, Any]) -> TestRecord:
    """Build restricted files record."""
    return _build_record(
        record_data,
        {
            "record": "public",
            "files": "restricted",
            "status": "restricted",
        },
    )


@pytest.fixture
def restricted_files_record_no_status(record_data: dict[str, Any]) -> TestRecord:
    """Build restricted files record with missing status field."""
    return _build_record(
        record_data,
        {
            "record": "public",
            "files": "restricted",
        },
    )
