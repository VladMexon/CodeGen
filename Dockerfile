FROM python:3.9-slim

# Отключаем буферизацию stdout/stderr — логи поступают сразу
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY script.py .
COPY data.html .


CMD ["python", "-u", "script.py"]
