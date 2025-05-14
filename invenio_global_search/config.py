# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2025 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Global Search Configs."""

from invenio_i18n import gettext as _

from .cli import rebuild_database_lom, rebuild_database_marc21, rebuild_database_rdm

GLOBAL_SEARCH_ORIGINAL_SCHEMAS = {
    "lom": {
        "schema": "lom",
        "name_l10n": _("OER"),
    },
    "rdm": {
        "schema": "rdm",
        "name_l10n": _("Research Result"),
    },
    "marc21": {
        "schema": "marc21",
        "name_l10n": _("Publication"),
    },
}
"""This configuration variable is to configure the schemas.

Setting up the configuration like that is only for convenience. Instances which
are not using all three packages should set this variable in invenio.cfg
"""

GLOBAL_SEARCH_REBUILD_DATABASE = [
    rebuild_database_rdm,
    rebuild_database_marc21,
    rebuild_database_lom,
]
"""This configuration variable is to configure the cli functions.

Setting up the configuration like that is only for convenience. Instances which
are not using all three packages should set this variable in invenio.cfg
"""
