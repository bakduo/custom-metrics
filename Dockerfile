FROM python:3.8-slim

LABEL maintainer="bakduo"

RUN apt-get update && apt-get install -y default-mysql-client && cd /tmp/ && pip install -U pip && mkdir /home/uapi && useradd --home-dir /home/uapi uapi && chown -R uapi:uapi /home/uapi

ENV PROJECT_DIR /home/uapi

WORKDIR ${PROJECT_DIR}

USER uapi

COPY Pipfile* ${PROJECT_DIR}/

RUN export PATH=$PATH:/home/uapi/.local/bin && pip install pipenv && pipenv lock --keep-outdated --requirements > /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY . ${PROJECT_DIR}/

VOLUME ["/home/uapi/app/config"]

EXPOSE 5000

CMD  python run.py
