import logging.config

from enterprise_subsidy.settings.utils import get_logger_config
from ..production import *

{% include "enterprisesubsidy/apps/settings/partials/common.py" %}

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ ENTERPRISE_SUBSIDY_OAUTH2_KEY }}"
BACKEND_SERVICE_EDX_OAUTH2_SECRET = "{{ ENTERPRISE_SUBSIDY_OAUTH2_SECRET }}"
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = "http://lms:8000/oauth2"

SOCIAL_AUTH_EDX_OAUTH2_KEY = "{{ ENTERPRISE_SUBSIDY_OAUTH2_KEY_SSO }}"
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "{{ ENTERPRISE_SUBSIDY_OAUTH2_SECRET_SSO }}"
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = SOCIAL_AUTH_EDX_OAUTH2_ISSUER + "/logout"

SOCIAL_AUTH_REDIRECT_IS_HTTPS = {% if ENABLE_HTTPS %}True{% else %}False{% endif %}

LMS_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"
ENTERPRISE_CATALOG_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ ENTERPRISE_CATALOG_HOST }}"
ENTERPRISE_SUBSIDY_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ ENTERPRISE_SUBSIDY_HOST }}"
FRONTEND_APP_LEARNING_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ MFE_HOST }}/learning"

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
