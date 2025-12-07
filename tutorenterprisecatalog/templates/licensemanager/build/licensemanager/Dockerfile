# syntax=docker/dockerfile:1.4
###### Minimal image with base system requirements for most stages
FROM docker.io/ubuntu:22.04 as minimal

ENV DEBIAN_FRONTEND=noninteractive
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && \
    apt install -y curl git-core language-pack-en python3 python3-dev \
    build-essential libcairo2 libffi-dev libmysqlclient-dev libxml2-dev libxslt-dev libjpeg-dev libssl-dev \
    pkg-config
ENV LC_ALL en_US.UTF-8

# Install pyenv and Python version
ARG PYTHON_VERSION=3.12.2
ENV PYENV_ROOT=/opt/pyenv
RUN git clone https://github.com/pyenv/pyenv $PYENV_ROOT --branch v2.3.36 --depth 1

# Install Python
RUN $PYENV_ROOT/bin/pyenv install $PYTHON_VERSION


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

# Create virtualenv
RUN $PYENV_ROOT/versions/$PYTHON_VERSION/bin/python -m venv /openedx/venv
ENV PATH="/openedx/venv/bin:$PATH"

RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install -r requirements/pip.txt

# Install python requirements
# This is identical to "make production-requirements" but it was split in multiple
# instructions to benefit from docker image caching
# Install base requirements
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install -r requirements/production.txt
# Install django-redis explicitly. Upstream uses memcached for caching, using redis to avoid another dep.
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install django-redis
{% for extra_requirement in LICENSE_MANAGER_EXTRA_PIP_REQUIREMENTS %}RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install '{{ extra_requirement }}'
{% endfor %}

FROM minimal AS license-manager-worker-dev

{{ patch("license-manager-worker-dockerfile-post-python-requirements") }}

ENV DJANGO_SETTINGS_MODULE license_manager.settings.tutor.celery_production
CMD celery --app=license_manager.celery:app worker -Q license_manager.default --loglevel=info

FROM minimal AS license-manager-bulk-enrollment-worker-dev

{{ patch("license-manager-bulk-enrollment-worker-dockerfile-post-python-requirements") }}

ENV DJANGO_SETTINGS_MODULE license_manager.settings.tutor.celery_production
CMD celery --app=license_manager.celery:app worker -Q license_manager.bulk_enrollment --loglevel=info

FROM minimal AS license-manager

{{ patch("license-manager-dockerfile-post-python-requirements") }}

# Collect static assets
COPY --chown=app:app assets.py ./license_manager/settings/assets.py
RUN DJANGO_SETTINGS_MODULE=license_manager.settings.assets make static

# Run production server
ENV DJANGO_SETTINGS_MODULE license_manager.settings.tutor.production
EXPOSE 18170
CMD gunicorn \
    --reload \
    --workers=2 \
    --name license_manager \
    -c /openedx/license-manager/license_manager/docker_gunicorn_configuration.py \
    --log-file - \
    --max-requests=1000 \
    license_manager.wsgi:application
