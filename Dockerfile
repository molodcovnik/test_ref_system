FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY ./app .

CMD python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --workers=1 --bind 0.0.0.0:8000 core.wsgi