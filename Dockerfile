FROM python:3.9
ENV APP_HOME=/app

WORKDIR ${APP_HOME}

EXPOSE 8080

COPY ./app /app
COPY requirements.txt .

RUN pip install -r requirements.txt
