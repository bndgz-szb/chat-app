FROM python:3.13.5-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8765

CMD ["python", "-u", "main.py"]
