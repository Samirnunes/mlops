FROM --platform=linux/amd64 python:3.12.6-slim

ENV PORT 80
ENV APP_NAME prefect_server
ENV WORKDIR /app

ENV PYTHONPATH ${WORKDIR}/${APP_NAME}
ENV PYTHONUNBUFFERED 1

WORKDIR ${WORKDIR}
EXPOSE ${PORT}

# System update
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd curl git wget bash && \
    rm -rf /var/lib/apt/lists/* /var/tmp/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry POETRY_VERSION=1.8.5 python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create true && \
    poetry config virtualenvs.path --unset && \
    poetry config virtualenvs.in-project true

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* ./


# Installing poetry dependencies
RUN poetry lock --no-update && \
    poetry install --no-root --only main

COPY . ./

RUN wget https://github.com/Droplr/aws-env/raw/master/bin/aws-env-linux-amd64 -O /app/aws-env
RUN chmod +x /app/aws-env

# Running app with FastAPI
RUN poetry run pip install "fastapi[standard]"
CMD ["/bin/bash", "-c", \
      "eval $(./aws-env) && \
      poetry run fastapi run \
      src/${APP_NAME}/api/app.py \
      --port ${PORT}"]
