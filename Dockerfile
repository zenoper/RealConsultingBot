FROM python:3.10.22-slim-bookworm

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt && python -m pip check

COPY . .

CMD ["python", "app.py"]
