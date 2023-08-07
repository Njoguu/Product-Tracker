FROM python:3.12.0b4-slim-bookworm AS builder

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "product_tracker/manage.py", "runserver", "0.0.0.0:8000" ]
