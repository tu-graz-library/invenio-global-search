# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Utils."""

from invenio_records_lom.utils import DotAccessWrapper


class LOMMetadata(DotAccessWrapper):
    """LOMMetadata."""

    def __init__(self, *, json=None) -> None:
        """Construct LOMMetadata."""
        super().__init__(data=json, overwritable=False)
