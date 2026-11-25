# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Components test."""

import pytest
from flask import Flask
from invenio_records.api import Record
from invenio_records_lom.utils import LOMMetadata
from invenio_records_marc21.services.record import Marc21Metadata

from invenio_global_search.components import (
    GlobalSearchSerializerType,
    map_metadata_from_a_to_b,
    map_metadata_from_a_to_b_many,
)

type SchemaConfig = tuple[
    str,
    GlobalSearchSerializerType,
    type[LOMMetadata | Marc21Metadata] | None,
]

SCHEMA_MAPPING = {
    "rdm": "records",
    "lom": "oer",
    "marc21": "publications",
}


def _assert_mapped_record(
    result: dict | None,
    record: Record,
    schema: str,
    expected_status: str,
) -> None:
    """Assert mapped global-search record structure and metadata."""
    assert result is not None
    assert "metadata" in result
    assert "original" in result

    original = result["original"]

    assert original["schema"] == schema
    assert original["pid"] == record["id"]
    assert original["created"] == record.dumps()["created"]
    assert original["access"]["status"] == expected_status
    assert original["view"] is not None

    assert isinstance(result["metadata"], dict)


@pytest.mark.parametrize(
    ("record_fixture", "expected_status"),
    [
        ("public_record", "open"),
        ("restricted_record", None),
        ("restricted_files_record", "restricted"),
    ],
    ids=["public", "full_restricted", "restricted_files"],
)
def test_map_metadata_from_a_to_b(
    appctx: Flask,  # noqa: ARG001
    request: pytest.FixtureRequest,
    schema_configuration: SchemaConfig,
    record_fixture: str,
    expected_status: str | None,
) -> None:
    """Test global-search simple mapping function."""
    schema, serializer_cls, metadata_cls = schema_configuration
    record: Record = request.getfixturevalue(record_fixture)

    result = map_metadata_from_a_to_b(
        record=record,
        serializer_cls=serializer_cls,
        schema=schema,
        metadata_cls=metadata_cls,
        schema_mapping=SCHEMA_MAPPING,
        include_links=False,
    )

    if expected_status is None:
        assert result is None
        return

    _assert_mapped_record(result, record, schema, expected_status)


@pytest.mark.parametrize(
    ("record_fixture", "expected_status"),
    [
        ("public_record", "open"),
        ("restricted_record", None),
        ("restricted_files_record", "restricted"),
    ],
    ids=["public", "full_restricted", "restricted_files"],
)
def test_map_metadata_from_a_to_b_many(
    appctx: Flask,  # noqa: ARG001
    request: pytest.FixtureRequest,
    schema_configuration: SchemaConfig,
    record_fixture: str,
    expected_status: str | None,
) -> None:
    """Test global-search batch mapping function."""
    schema, serializer_cls, metadata_cls = schema_configuration
    record: Record = request.getfixturevalue(record_fixture)
    records = [record, record]

    results = map_metadata_from_a_to_b_many(
        records=records,
        serializer_cls=serializer_cls,
        schema=schema,
        metadata_cls=metadata_cls,
        schema_mapping=SCHEMA_MAPPING,
        include_links=False,
    )

    if expected_status is None:
        assert results is None
        return

    assert results is not None
    assert len(results) == len(records)

    for result in results:
        _assert_mapped_record(result, record, schema, expected_status)
