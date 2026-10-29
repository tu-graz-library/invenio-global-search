# SPDX-FileCopyrightText: 2023-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Global Search for InvenioRDM."""

from .components import (
    LOMToGlobalSearchComponent,
    Marc21ToGlobalSearchComponent,
    RDMToGlobalSearchComponent,
)
from .ext import InvenioGlobalSearch

__version__ = "0.8.0"

__all__ = (
    "__version__",
    "InvenioGlobalSearch",
    "LOMToGlobalSearchComponent",
    "Marc21ToGlobalSearchComponent",
    "RDMToGlobalSearchComponent",
)
