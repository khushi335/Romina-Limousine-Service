import os
import sys

# Path to your project directory
PROJECT_DIR = "/home/hightech/rominalimousineservice.com/service"
VENV_DIR = "/home/hightech/virtualenv/rominalimousineservice.com/service/3.10"

# Add project directory to Python path
sys.path.insert(0, PROJECT_DIR)

# Activate virtual environment
activate_this = os.path.join(VENV_DIR, "bin/activate_this.py")
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()