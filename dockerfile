FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev sqlite3 && \
    rm- rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860
# EXPOSE 8000  
#(for flask)

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app.main:app"]

# (for flask)
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.main:app"]
