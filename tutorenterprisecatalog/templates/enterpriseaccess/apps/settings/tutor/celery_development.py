import logging.config

from enterprise_access.settings.utils import get_logger_config
from ..local import *

{% include "enterpriseaccess/apps/settings/partials/common.py" %}

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ ENTERPRISE_ACCESS_OAUTH2_KEY_DEV }}"
BACKEND_SERVICE_EDX_OAUTH2_SECRET = "{{ ENTERPRISE_ACCESS_OAUTH2_SECRET }}"
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = "http://lms:8000/oauth2"

SOCIAL_AUTH_EDX_OAUTH2_KEY = "{{ ENTERPRISE_ACCESS_OAUTH2_KEY_SSO_DEV }}"
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "{{ ENTERPRISE_ACCESS_OAUTH2_SECRET_SSO }}"
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = "http://{{ LMS_HOST }}:8000"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = SOCIAL_AUTH_EDX_OAUTH2_ISSUER + "/logout"

ECOMMERCE_URL = "http://{{ ECOMMERCE_HOST }}:8130"
LICENSE_MANAGER_URL = "http://{{ LICENSE_MANAGER_HOST }}:8170"
LMS_URL = "http://{{ LMS_HOST }}:8000"
DISCOVERY_URL = "http://{{ DISCOVERY_HOST }}:8381"
ENTERPRISE_LEARNER_PORTAL_URL = "http://{{ MFE_HOST }}:8734/learner-portal-enterprise"
ENTERPRISE_ADMIN_PORTAL_URL = "http://{{ MFE_HOST }}:1991/admin-portal-enterprise"
ENTERPRISE_CATALOG_URL = "http://{{ ENTERPRISE_CATALOG_HOST }}:8160"
ENTERPRISE_SUBSIDY_URL = "http://{{ ENTERPRISE_SUBSIDY_HOST }}:8280"
ENTERPRISE_ACCESS_URL = "http://{{ ENTERPRISE_ACCESS_HOST }}:8270"

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
