# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Utils."""

from invenio_rdm_records.services import RDMRecordServiceConfig
from invenio_records_lom.services import LOMRecordServiceConfig
from invenio_records_marc21.services import Marc21RecordServiceConfig

schema_mapping = {
    "rdm": RDMRecordServiceConfig,
    "lom": LOMRecordServiceConfig,
    "marc21": Marc21RecordServiceConfig,
}
