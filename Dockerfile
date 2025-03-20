FROM python:3.12-slim as python-base

ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m venv $VIRTUAL_ENV \
    && pip install --upgrade pip wheel setuptools

FROM python-base as builder

WORKDIR /loan_advisory_service

COPY pyproject.toml .
COPY loan_advisory_service /loan_advisory_service/

RUN pip install --no-cache-dir .

FROM python-base

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

COPY loan_advisory_service /loan_advisory_service/
COPY alembic.ini .
COPY 1280173589_j7ukhvm5_config.json .
