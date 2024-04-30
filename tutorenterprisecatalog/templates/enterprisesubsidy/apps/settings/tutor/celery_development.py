import logging.config

from enterprise_subsidy.settings.utils import get_logger_config
from ..local import *

{% include "enterprisesubsidy/apps/settings/partials/common.py" %}

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ ENTERPRISE_SUBSIDY_OAUTH2_KEY_DEV }}"
BACKEND_SERVICE_EDX_OAUTH2_SECRET = "{{ ENTERPRISE_SUBSIDY_OAUTH2_SECRET }}"
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = "http://lms:8000/oauth2"

SOCIAL_AUTH_EDX_OAUTH2_KEY = "{{ ENTERPRISE_SUBSIDY_OAUTH2_KEY_SSO_DEV }}"
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "{{ ENTERPRISE_SUBSIDY_OAUTH2_SECRET_SSO }}"
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = "http://{{ LMS_HOST }}:8000"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = SOCIAL_AUTH_EDX_OAUTH2_ISSUER + "/logout"

LMS_URL = "http://{{ LMS_HOST }}:8000"
ENTERPRISE_CATALOG_URL = "http://{{ ENTERPRISE_CATALOG_HOST }}:8160"
ENTERPRISE_SUBSIDY_URL = "http://{{ ENTERPRISE_SUBSIDY_HOST }}:8280"
FRONTEND_APP_LEARNING_URL = "http://{{ MFE_HOST }}:2000/learning"

# Logging: get rid of local handler
logging_config = get_logger_config(debug=False)
if "local" in logging_config["handlers"]:
    logging_config["handlers"].pop("local")
for logger in logging_config["loggers"].values():
    try:
        logger["handlers"].remove("local")
    except ValueError:
        continue
logging.config.dictConfig(logging_config)
