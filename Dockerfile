FROM python:3.11-slim

WORKDIR /code


ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'


# Install basic SO and Python
RUN apt-get update --fix-missing \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    wget curl vim locales zip unzip apt-utils \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uWSGI==2.0.25.1 uwsgitop==0.12

# Replace shell with bash so we can source files
SHELL ["/bin/bash", "-c"]
RUN echo "export LS_OPTIONS='--color=auto'" >>~/.bashrc && \
    echo "eval "\`dircolors\`"" >>~/.bashrc && \
    echo "alias ls='ls \$LS_OPTIONS'" >>~/.bashrc && \
    echo "alias ll='ls \$LS_OPTIONS -l'" >>~/.bashrc && \
    echo "alias l='ls \$LS_OPTIONS -lA'" >>~/.bashrc

#### Prepare BACKEND Django API

COPY pyproject.toml ./
RUN pip install poetry
RUN poetry install --no-dev


ENV PYTHONUNBUFFERED=1 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONIOENCODING=UTF-8
ENV SHELL=/bin/bash LANG=en_US.UTF-8

# Gets the current git commit hash
ARG GIT_HASH
ENV GIT_HASH=$GIT_HASH

COPY . ./

EXPOSE 8000


CMD ["gunicorn", "--bind", ":8000", "--workers", "1", "geotracking.geotracking.wsgi"]

