FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY baitap_11.py .

CMD ["uvicorn", "baitap_11:app", "--host", "0.0.0.0", "--port", "8000"]