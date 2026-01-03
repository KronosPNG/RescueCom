FROM python:3.14-slim

WORKDIR /app

COPY ./cloud/requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

RUN adduser --no-create-home user
USER user

ENV PYTHONPATH=.

COPY ./cloud .
COPY ./common ./common

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
