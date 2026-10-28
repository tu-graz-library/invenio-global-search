# SPDX-FileCopyrightText: 2023-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Global Search Configs."""

from invenio_i18n import gettext as _

from .tasks import (
    rebuild_database_lom,
    rebuild_database_marc21,
    rebuild_database_rdm,
    update_missing_lom,
    update_missing_marc21,
    update_missing_rdm,
)

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
"""This configuration variable is to configure the rebuild-database cli functions.

Setting up the configuration like that is only for convenience. Instances which
are not using all three packages should set this variable in invenio.cfg
"""

GLOBAL_SEARCH_UPDATE_MISSING = [
    update_missing_rdm,
    update_missing_marc21,
    update_missing_lom,
]
"""This configuration variable is to configure the update missing records cli functions.

Setting up the configuration like that is only for convenience. Instances which
are not using all three packages should set this variable in invenio.cfg
"""
