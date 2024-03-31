# Use the official Python image from the Docker Hub
FROM python:3.12 as poetry

RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt

FROM python:3.12
ENV DEBUG=False
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY --from=poetry /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./chat ./chat

CMD ["python", "-m", "gunicorn", "-b", "0.0.0.0:80", "chat.asgi:application", "-k", "uvicorn.workers.UvicornWorker"]
