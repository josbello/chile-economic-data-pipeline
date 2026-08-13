FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

RUN mkdir -p data/raw data/processed

CMD ["sh", "-c", "python src/extract.py && python src/transform.py && python src/load.py"]