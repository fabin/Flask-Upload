import sae

from upload import app

application = sae.create_wsgi_app(app)