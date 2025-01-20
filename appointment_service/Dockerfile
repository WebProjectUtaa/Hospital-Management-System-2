FROM python:3.10.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt ./requirements.txt
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
