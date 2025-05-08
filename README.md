# invenio-global-search

# Installation
This basic installation of this package  ```pip install invenio-global-search``` will not give access to any of its features. It is intended to be extended with the packages needed in a specific invenio instance. There are 3 packages handled by _invenio-global-search_:
- rdm-records
- lom (OER)
- marc21 (Publications)

To install any of them or all:

- ```pip install invenio-global-search[rdm]``` - this enables the rdm-records features.
- ```pip install invenio-global-search[rdm, marc21, lom]``` - this enables all the features of the package.


# Configuration

Add following code blocks to the invenio.cfg file:

## Components

If all packages mentioned above are installed, simply add:

```python
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
```

If there is a chance that one of them is not installed, this can be handled with ```try-except```:

```python
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
```

## Search template

```python
SEARCH_UI_SEARCH_TEMPLATE = "invenio_records_dublin_core/search/search.html"

from invenio_search_ui.views import blueprint
from flask import render_template

@blueprint.route("/records/search")
def records_search():
    """Search page ui."""
    return render_template("invenio_app_rdm/records/search.html")
```

## Schema

As mentioned for components, if all packages are installed, add:
```python
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
```

If one or more is missing, simply remove the entry for the respective package.
