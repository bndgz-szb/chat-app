FROM python:3.13.5-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY server.py .

CMD python3 server.py

EXPOSE 8765