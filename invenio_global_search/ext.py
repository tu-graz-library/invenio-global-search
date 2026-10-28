# SPDX-FileCopyrightText: 2023-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Global Search for InvenioRDM."""

from flask import Flask

from . import config


class InvenioGlobalSearch:
    """InvenioGlobalSearch."""

    def __init__(self, app: Flask) -> None:
        """Construct InvenioGlobalSearch."""
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["invenio-global-search"] = self

    @staticmethod
    def init_config(app: Flask) -> None:
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("GLOBAL_SEARCH_"):
                app.config.setdefault(k, getattr(config, k))
