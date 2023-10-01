# invenio-global-search

# configuration

add following code to the invenio.cfg file

from invenio_search_ui.views import blueprint
from invenio_rdm_records.services.components import DefaultRecordsComponents
from invenio_global_search.components import RDMToDublinCoreComponent
from flask import render_template

RDM_RECORDS_SERVICE_COMPONENTS = DefaultRecordsComponents + [RDMToDublinCoreComponent]

SEARCH_UI_SEARCH_TEMPLATE = "invenio_records_dublin_core/search/search.html"

@blueprint.route("/records/search")
def records_search():
    """Search page ui."""
    return render_template("invenio_app_rdm/records/search.html")
