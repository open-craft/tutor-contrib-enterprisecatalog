from ..production import *

{% include "enterpriseaccess/apps/settings/partials/common.py" %}

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ ENTERPRISE_ACCESS_OAUTH2_KEY }}"
BACKEND_SERVICE_EDX_OAUTH2_SECRET = "{{ ENTERPRISE_ACCESS_OAUTH2_SECRET }}"
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = "http://lms:8000/oauth2"

SOCIAL_AUTH_EDX_OAUTH2_KEY = "{{ ENTERPRISE_ACCESS_OAUTH2_KEY_SSO }}"
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "{{ ENTERPRISE_ACCESS_OAUTH2_SECRET_SSO }}"
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = SOCIAL_AUTH_EDX_OAUTH2_ISSUER + "/logout"

SOCIAL_AUTH_REDIRECT_IS_HTTPS = {% if ENABLE_HTTPS %}True{% else %}False{% endif %}

ECOMMERCE_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ ECOMMERCE_HOST }}"
LICENSE_MANAGER_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LICENSE_MANAGER_HOST }}"
LMS_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"
DISCOVERY_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ DISCOVERY_HOST }}"
ENTERPRISE_LEARNER_PORTAL_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ MFE_HOST }}/learner-portal-enterprise"
ENTERPRISE_ADMIN_PORTAL_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ MFE_HOST }}/admin-portal-enterprise"
ENTERPRISE_CATALOG_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ ENTERPRISE_CATALOG_HOST }}"
ENTERPRISE_SUBSIDY_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ ENTERPRISE_SUBSIDY_HOST }}"
ENTERPRISE_ACCESS_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ ENTERPRISE_ACCESS_HOST }}"

CORS_ORIGIN_WHITELIST = list(CORS_ORIGIN_WHITELIST) + [
    "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ MFE_HOST }}",
]
CSRF_TRUSTED_ORIGINS.append("{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ MFE_HOST }}")

{{ patch("enterprise-access-production-settings") }}
