# SPDX-FileCopyrightText: 2023-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Helper proxy to the state object."""

from flask import current_app
from werkzeug.local import LocalProxy

current_global_search = LocalProxy(
    lambda: current_app.extensions["invenio-global-search"],
)
"""Helper proxy to get the global search extension."""
