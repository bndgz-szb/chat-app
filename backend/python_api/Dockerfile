FROM python:3.13.5-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "python_api.main:app"]
