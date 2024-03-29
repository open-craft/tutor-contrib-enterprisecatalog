{% if is_buildkit_enabled() %}# syntax=docker/dockerfile:1.4{% endif %}
###### Minimal image with base system requirements for most stages
FROM docker.io/ubuntu:20.04 as minimal

ENV DEBIAN_FRONTEND=noninteractive
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked{% endif %} \
    apt update && \
    apt install -y curl git-core language-pack-en python3 python3-pip python3-venv \
    build-essential libcairo2 libffi-dev libmysqlclient-dev libxml2-dev libxslt-dev libjpeg-dev libssl-dev
ENV LC_ALL en_US.UTF-8

ARG APP_USER_ID=1000
RUN if [ "$APP_USER_ID" = 0 ]; then echo "app user may not be root" && false; fi
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

###### Git-clone license-manager repo
ARG LICENSE_MANAGER_REPOSITORY='{{ LICENSE_MANAGER_REPOSITORY }}'
ARG LICENSE_MANAGER_VERSION='{{ LICENSE_MANAGER_REPOSITORY_VERSION }}'
RUN mkdir -p /openedx/license-manager && \
    git clone $LICENSE_MANAGER_REPOSITORY --branch $LICENSE_MANAGER_VERSION --depth 1 /openedx/license-manager
WORKDIR /openedx/license-manager

# Setup empty yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV LICENSE_MANAGER_CFG /openedx/config.yml

# Install python venv
RUN python3 -m venv ../venv/
ENV PATH="/openedx/venv/bin:$PATH"

RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}pip install \
    # https://pypi.org/project/setuptools/
    # https://pypi.org/project/pip/
    # https://pypi.org/project/wheel/
    setuptools==67.7.2 pip==23.1.2. wheel==0.40.0

# Install python requirements
# This is identical to "make production-requirements" but it was split in multiple
# instructions to benefit from docker image caching
# Install base requirements
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}pip install -r requirements.txt
{% for extra_requirement in LICENSE_MANAGER_EXTRA_PIP_REQUIREMENTS %}RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}pip install '{{ extra_requirement }}'
{% endfor %}

# Install extra requirements
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}pip install \
    # Use redis as a django cache https://pypi.org/project/django-redis/
    django-redis==5.2.0

FROM minimal AS license-manager-worker-dev

{{ patch("license-manager-worker-dockerfile-post-python-requirements") }}

ENV WORKER_CONFIGURATION_MODULE license_manager.settings.tutor.celery_production
CMD celery --app=license_manager.celery:app worker -Q license_manager.default --loglevel=info

FROM minimal AS license-manager-bulk-enrollment-worker-dev

{{ patch("license-manager-bulk-enrollment-worker-dockerfile-post-python-requirements") }}

ENV WORKER_CONFIGURATION_MODULE license_manager.settings.tutor.celery_production
CMD celery --app=license_manager.celery:app worker -Q license_manager.bulk_enrollment --loglevel=info

FROM minimal AS license-manager

# Install uwsgi
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}pip install \
    # uwsgi server https://pypi.org/project/uWSGI/
    uwsgi==2.0.21


{{ patch("license-manager-dockerfile-post-python-requirements") }}

# Collect static assets
RUN make static

# Run production server
ENV DJANGO_SETTINGS_MODULE license_manager.settings.tutor.production
EXPOSE 8000
CMD uwsgi \
    --static-map /static=/openedx/license-manager/license_manager/assets \
    --http 0.0.0.0:8000 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=2 \
    --buffer-size=8192 \
    --wsgi-file license_manager/wsgi.py
