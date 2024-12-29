FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1

RUN apt-get update \
    && apt-get install curl -y \
    && curl -sSL https://install.python-poetry.org | python - --version 1.7.0

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app/web/

COPY ./pyproject.toml ./poetry.lock /app/web/

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY ./apps/base/ .

EXPOSE 8000

#CMD [ "poetry", "run", "gunicorn", "-b", "0.0.0.0:8000"]
