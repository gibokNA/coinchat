FROM python:3.11.6-slim

RUN apt-get update && apt-get install -y build-essential

WORKDIR /app
COPY . /app

RUN pip install poetry

RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "daphne", "-b", "0.0.0.0", "-p", "8000", "coinchat_backend_channels.asgi:application"]