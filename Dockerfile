FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Railway will provide the PORT environment variable
CMD ["sh", "-c", "gunicorn server.run:app --bind 0.0.0.0:$PORT --workers 2"]