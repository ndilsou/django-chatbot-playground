# Use the official Python image from the Docker Hub
FROM python:3.12 as builder

RUN pip install poetry
WORKDIR /build
COPY pyproject.toml poetry.lock ./
RUN mkdir -p /var/task/ \
    && poetry export -f requirements.txt --output requirements.txt \
    && pip install --no-cache-dir -r requirements.txt  -t /var/task/

FROM python:3.12

ENV DEBUG=False
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /var/task
COPY --from=builder /var/task /var/task
COPY ./chat ./chat

CMD ["python", "-m", "gunicorn", "-b", "0.0.0.0:80", "chat.asgi:application", "-k", "uvicorn.workers.UvicornWorker"]
