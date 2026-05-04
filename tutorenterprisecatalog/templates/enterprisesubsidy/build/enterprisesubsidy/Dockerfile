# syntax=docker/dockerfile:1.4
###### Minimal image with base system requirements for most stages
FROM docker.io/ubuntu:22.04 as minimal

ENV DEBIAN_FRONTEND=noninteractive
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && \
    apt install -y curl git-core language-pack-en python3 python3-dev \
    build-essential libcairo2 libffi-dev libmysqlclient-dev libxml2-dev libxslt-dev libjpeg-dev libssl-dev \
    pkg-config libbz2-dev liblzma-dev

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

###### Git-clone enterprise-subsidy repo
ARG ENTERPRISE_SUBSIDY_REPOSITORY='{{ ENTERPRISE_SUBSIDY_REPOSITORY }}'
ARG ENTERPRISE_SUBSIDY_VERSION='{{ ENTERPRISE_SUBSIDY_REPOSITORY_VERSION }}'
RUN mkdir -p /openedx/enterprise-subsidy && \
    git clone $ENTERPRISE_SUBSIDY_REPOSITORY --branch $ENTERPRISE_SUBSIDY_VERSION /openedx/enterprise-subsidy
WORKDIR /openedx/enterprise-subsidy

{%- if ENTERPRISE_SUBSIDY_REPOSITORY_COMMIT %}
RUN git checkout {{ ENTERPRISE_SUBSIDY_REPOSITORY_COMMIT }}
{% endif %}

# Setup empty yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV ENTERPRISE_SUBSIDY_CFG /openedx/config.yml

# Create virtualenv
RUN $PYENV_ROOT/versions/$PYTHON_VERSION/bin/python -m venv /openedx/venv
ENV PATH="/openedx/venv/bin:$PATH"

RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install -r requirements/pip.txt

# TODO: Remove this once tzdata is added in the upstream requirements
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install tzdata

# Install python requirements
# This is identical to "make production-requirements" but it was split in multiple
# instructions to benefit from docker image caching
# Install base requirements
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install -r requirements/production.txt
# Install django-redis explicitly. Upstream uses memcached for caching, using redis to avoid another dep.
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install django-redis
{% for extra_requirement in ENTERPRISE_SUBSIDY_EXTRA_PIP_REQUIREMENTS %}RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install '{{ extra_requirement }}'
{% endfor %}

FROM minimal AS enterprise-subsidy

{{ patch("enterprise-subsidy-dockerfile-post-python-requirements") }}

RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install uwsgi==2.0.30

# Collect static assets
COPY --chown=app:app assets.py ./enterprise_subsidy/settings/assets.py
RUN DJANGO_SETTINGS_MODULE=enterprise_subsidy.settings.assets make static

# Run production server
ENV DJANGO_SETTINGS_MODULE enterprise_subsidy.settings.tutor.production
EXPOSE 8000
CMD uwsgi \
    --static-map /static=/openedx/enterprise-subsidy/assets \
    --http 0.0.0.0:8000 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=2 \
    --buffer-size=8192 \
    --wsgi-file enterprise_subsidy/wsgi.py
