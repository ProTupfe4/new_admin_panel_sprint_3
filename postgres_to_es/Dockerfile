FROM python:latest as builder
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_ROOT_USER_ACTION=ignore \
  DOCKERIZE_VERSION="v0.7.0"

WORKDIR /opt/app

RUN apt-get update  \
    && apt-get -y install netcat-traditional \
    curl \
    git  \
    wget \
    && wget -O - https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz | tar xzf - -C /usr/local/bin \
    && apt-get autoremove -yqq --purge wget && rm -rf /var/lib/apt/lists/*

RUN groupadd -r django && useradd -d /opt/app -r -g django django \
    && chown django:django -R /opt/app/

COPY --chown=django:django requirements.txt .
COPY --chown=django:django entrypoint.sh .
COPY --chown=django:django movies.json .


RUN  python -m pip install --upgrade pip \
     && pip install -r --no-cache-dir requirements.txt \
     && chmod +x entrypoint.sh


COPY . .


USER django

ENTRYPOINT ["./entrypoint.sh"]