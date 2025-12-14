FROM public.ecr.aws/docker/library/python:3.12-slim

WORKDIR /app

# Install dependencies
RUN --mount=type=cache,id=apt-lists,target=/var/lib/apt/lists,sharing=locked \
    --mount=type=cache,id=apt-cache,target=/var/cache/apt,sharing=locked \
    set -eux; \
    apt update; \
    apt install -y libreoffice poppler-utils curl && \
    rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN cp -p /root/.local/bin/uv /usr/local/bin/uv
RUN cp -p /root/.local/bin/uvx /usr/local/bin/uvx

# Install from requirements file
COPY ./pyproject.toml ./uv.lock ./

RUN mkdir src
RUN --mount=type=cache,target=/root/.cache/uv uv add "aws_opentelemetry_distro_genai_beta>=0.1.6"
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --no-editable

# Copy entire project (respecting .dockerignore)
COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --no-editable

# Create non-root user
RUN useradd -m -u 1000 bedrock_agentcore

# Set Run Settings
USER bedrock_agentcore

ENV DOCKER_CONTAINER=1
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

EXPOSE 8080

CMD ["opentelemetry-instrument", "python", "-m", "agents"]
