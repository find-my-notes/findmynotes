import os
from django.core.wsgi import get_wsgi_application
# from whitenoise import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FindMyNotes.settings")
application = get_wsgi_application()
# application = DjangoWhiteNoise(get_wsgi_application())
