# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Components to Hook into other data models."""

from __future__ import annotations

from flask_principal import Identity
from invenio_records_dublin_core import DublinCoreRecord, current_records_dublin_core
from invenio_records_resources.services.records.components import ServiceComponent


class Marc21ToDublinCoreComponent(ServiceComponent):
    """Marc21ToDublinCoreComponent."""


class LOMToDublinCoreComponent(ServiceComponent):
    """LOMToDublinCoreComponent."""


class RDMToDublinCoreComponent(ServiceComponent):
    """RDMToDublinCoreComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,
        record: DublinCoreRecord | None = None,
        **kwargs: dict,
    ) -> None:
        """Create handler."""
        title = record.metadata["title"]
        data = {
            "metadata": {
                "title": title,
            },
        }
        current_records_dublin_core.record_service.create(
            identity=identity,
            data=data,
        )
