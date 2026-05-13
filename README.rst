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

Further documentation is available on
https://invenio-global-search.readthedocs.io/

Tests
-----

.. code-block:: console

    pipenv run ./run-tests.sh


OpenAIRE Indexing
-----

ListRecords & GetRecord features
+++++++++


An InvenioRDM repository can be harvested via the Open Archives Initiative Protocol for Metadata Harvesting (OAI-PMH). OAI-PMH is a widely used protocol for harvesting metadata and most popular repository software provide support for this protocol.

Because Global search needs to support multiple data models, the default OAISERVER_ features had to be overridden with custom function and classes that are based mostly on `global-search` index. This works also because global-search keeps track only of open-access records.

Currently supported custom OAI Features:
  - ListRecords and GetRecord for

    - metadataPrefix = oai_dc -> records from all 3 data models are serialized
    - metadataPrefix = lom -> only OER records are serialized
    - metadataPrefix = marc21 -> only Publication records are serialized

Access these by searching for the endpoint `/oai2d` and adding params like `?verb=ListRecords`. Examples:

 - `https://invenio-test.tugraz.at/oai2d?verb=ListRecords&metadataPrefix=marc21`
 - `https://invenio-test.tugraz.at/oai2d?verb=GetRecord&identifier=oai:invenio-test.tugraz.at:46t12-eng12&metadataPrefix=marc21`


Sets
+++++++++
  TODO

