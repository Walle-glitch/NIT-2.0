# NIT-2.0/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Kopiera bara requirements först för att cache:a install
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Kopiera all övrig kod (inklusive _Bot_Config.py, Internal_Modules osv)
COPY . .

CMD ["python3", "main.py"]
