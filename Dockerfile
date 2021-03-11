FROM python:3.8-alpine

WORKDIR /home/app

COPY . .

RUN python -m venv venv

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN venv/bin/pip install -e .

RUN venv/bin/pip install gunicorn

RUN chmod +x ./boot.sh

EXPOSE 2000

ENTRYPOINT ["./boot.sh"]
