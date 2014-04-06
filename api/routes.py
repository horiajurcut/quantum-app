from api.core import app

from api.controllers.login import *
from api.controllers.dashboard import *
from api.controllers.nlp import *
from api.controllers.github import *

import traceback

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404
