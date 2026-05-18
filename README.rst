..
    Copyright (C) 2023 Graz University of Technology.

    invenio-global-search is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.


======================
 invenio-global-search
======================

.. image:: https://github.com/tu-graz-library/invenio-global-search/workflows/CI/badge.svg
        :target: https://github.com/tu-graz-library/invenio-global-search/actions?query=workflow%3ACI

.. image:: https://img.shields.io/github/tag/tu-graz-library/invenio-global-search.svg
        :target: https://github.com/tu-graz-library/invenio-global-search/releases

.. image:: https://img.shields.io/pypi/dm/invenio-global-search.svg
        :target: https://pypi.python.org/pypi/invenio-global-search

.. image:: https://img.shields.io/github/license/tu-graz-library/invenio-global-search.svg
        :target: https://github.com/tu-graz-library/invenio-global-search/blob/master/LICENSE

Dublin Core data model for InvenioRDM


Tests
-----

.. code-block:: console

    uv run ./run-tests.sh


Installation
============

This basic installation of this package::

    uv pip install invenio-global-search

will not give access to any of its features. It is intended to be extended
with the packages needed in a specific Invenio instance.

There are 3 packages handled by ``invenio-global-search``:

- ``rdm-records``
- ``lom`` (OER)
- ``marc21`` (Publications)

To install any of them or all:

- ::

      uv pip install invenio-global-search[rdm]

  This enables the ``rdm-records`` features.

- ::

      uv pip install invenio-global-search[rdm, marc21, lom]

  This enables all the features of the package.


Configuration
=============

Add the following code blocks to the ``invenio.cfg`` file.


Components
----------

If all packages mentioned above are installed, simply add:

.. code-block:: python

    from invenio_rdm_records.services.components import DefaultRecordsComponents
    from invenio_global_search.components import (
        LOMToGlobalSearchComponent,
        Marc21ToGlobalSearchComponent,
        RDMToGlobalSearchComponent,
    )

    from invenio_rdm_records.services.components import (
        DefaultRecordsComponents as RDMDefaultRecordsComponents,
    )
    from invenio_records_lom.services.components import (
        DefaultRecordsComponents as LOMDefaultRecordsComponents,
    )
    from invenio_records_marc21.services.components import (
        DefaultRecordsComponents as Marc21DefaultRecordsComponents,
    )


    RDM_RECORDS_SERVICE_COMPONENTS = RDMDefaultRecordsComponents + [
        RDMToGlobalSearchComponent
    ]
    LOM_RECORDS_SERVICE_COMPONENTS = LOMDefaultRecordsComponents + [
        LOMToGlobalSearchComponent
    ]
    MARC21_RECORDS_SERVICE_COMPONENTS = Marc21DefaultRecordsComponents + [
        Marc21ToGlobalSearchComponent
    ]

If there is a chance that one of them is not installed, this can be handled
with ``try-except``:

.. code-block:: python

    try:
        from invenio_records_marc21.services.components import (
            DefaultRecordsComponents as Marc21DefaultRecordsComponents,
        )
    except ImportError:
        Marc21DefaultRecordsComponents = None

    if Marc21DefaultRecordsComponents is not None:
        MARC21_RECORDS_SERVICE_COMPONENTS = Marc21DefaultRecordsComponents + [
            Marc21ToGlobalSearchComponent
        ]
    else:
        MARC21_RECORDS_SERVICE_COMPONENTS = [Marc21ToGlobalSearchComponent]


Search template
---------------

.. code-block:: python

    SEARCH_UI_SEARCH_TEMPLATE = "invenio_records_dublin_core/search/search.html"

    from invenio_search_ui.views import blueprint
    from flask import render_template

    @blueprint.route("/records/search")
    def records_search():
        """Search page ui."""
        return render_template("invenio_app_rdm/records/search.html")


Schema
------

As mentioned for components, if all packages are installed, add:

.. code-block:: python

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

If one or more is missing, simply remove the entry for the respective package.


OpenAIRE Indexing
-----------------

ListRecords & GetRecord features
================================


An InvenioRDM repository can be harvested via the Open Archives Initiative Protocol for Metadata Harvesting (OAI-PMH). OAI-PMH is a widely used protocol for harvesting metadata and most popular repository software provide support for this protocol.

Because Global search needs to support multiple data models, the default `OAISERVER_` features had to be overridden with custom function and classes that are based mostly on `global-search` index. This works also because global-search keeps track only of open-access records.

Currently supported custom OAI Features:
  - ListRecords and GetRecord for

    - metadataPrefix = oai_dc -> records from all 3 data models are serialized
    - metadataPrefix = lom -> only OER records are serialized
    - metadataPrefix = marc21 -> only Publication records are serialized

Access these by searching for the endpoint `/oai2d` and adding params like `?verb=ListRecords`. Examples:

 - `https://yourinvenio.com/oai2d?verb=ListRecords&metadataPrefix=marc21`
 - `https://yourinvenio.com/oai2d?verb=GetRecord&identifier=oai:yourinvenio.com:46t12-eng12&metadataPrefix=marc21`


Sets
====
  TODO


Further documentation is available on
https://invenio-global-search.readthedocs.io/
