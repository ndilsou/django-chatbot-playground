FROM public.ecr.aws/lambda/python:3.12 as builder

RUN pip install poetry
WORKDIR /build
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt \
    && pip install --no-cache-dir -r requirements.txt -t ${LAMBDA_TASK_ROOT}

# ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
# RUN /install.sh && rm /install.sh

FROM public.ecr.aws/lambda/python:3.12

ENV DEBUG=False
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=builder ${LAMBDA_TASK_ROOT} ${LAMBDA_TASK_ROOT}
COPY . ${LAMBDA_TASK_ROOT}

CMD ["chat.awslambda.handler"]