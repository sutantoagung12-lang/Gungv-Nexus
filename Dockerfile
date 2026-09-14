FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY nexus ./nexus
COPY config ./config
RUN pip install --no-cache-dir .
ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "uvicorn nexus.api:app --host 0.0.0.0 --port ${PORT}"]
