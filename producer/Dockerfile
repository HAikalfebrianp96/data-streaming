FROM python:3.11

WORKDIR /app

RUN pip install --no-cache-dir pandas confluent-kafka

COPY movies_producer.py .

CMD ["python", "movies_producer.py"]
