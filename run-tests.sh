#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2019-2020 CERN.
# SPDX-FileCopyrightText: 2019-2020 Northwestern University.
# SPDX-FileCopyrightText: 2021 TU Wien.
# SPDX-FileCopyrightText: 2023-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

ruff check .
ty check .

python -m pytest

