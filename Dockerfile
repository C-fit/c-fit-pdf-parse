FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml .

# pyproject.toml 기반으로 모든 의존성 설치 및 lock 파일 생성
RUN uv pip install --system \
    -r pyproject.toml \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    --index-strategy unsafe-best-match

COPY ./src ./src

ENV PORT=8000
EXPOSE ${PORT}

CMD exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${PORT} src.main:app
