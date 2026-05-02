FROM python:3.11.4-slim

WORKDIR /erp

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# instalando as denpendecia da lib Weasyprint
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py seed && gunicorn app.wsgi --bind 0.0.0.0:8000"]