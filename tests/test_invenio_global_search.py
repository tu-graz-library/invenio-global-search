# SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Module tests."""

from flask import Flask

from invenio_global_search import InvenioGlobalSearch, __version__


def test_version() -> None:
    """Test version import."""
    assert __version__  # ty: ignore[redundant-condition]


def test_init() -> None:
    """Test extension initialization."""
    app = Flask("testapp")
    _ = InvenioGlobalSearch(app)
    assert "invenio-global-search" in app.extensions
