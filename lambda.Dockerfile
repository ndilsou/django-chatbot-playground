FROM python:3.12 as poetry

RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt

# Use an AWS base image
FROM public.ecr.aws/lambda/python:3.12
# ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
# RUN /install.sh && rm /install.sh

# Copy your Django project
COPY . /var/task/

# Install dependencies
COPY --from=poetry /app/requirements.txt .

# RUN /root/.cargo/bin/uv pip install --system --no-cache -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run your script
CMD ["chat.awslambda.handler"]