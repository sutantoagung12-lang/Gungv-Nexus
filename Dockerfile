FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY . .
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
CMD ["python", "-m", "runtime.nexus_daemon"]
