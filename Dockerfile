FROM python:3.14-slim

WORKDIR /app

COPY ./cloud/requirements.txt requirements.txt

RUN python -m pip install --upgrade pip setuptools
RUN python -m pip install -v -r requirements.txt

RUN addgroup --gid 1000 appgroup
RUN adduser --gid 1000 --uid 1000 \
			--disabled-password \
			--disabled-login \
			--no-create-home appuser

COPY --from=tianon/gosu /gosu /usr/local/bin/

COPY ./common ./common
COPY ./cloud/entrypoint.sh ./entrypoint.sh
COPY ./cloud/gunicorn_config.py ./gunicorn_config.py
COPY ./cloud ./cloud

RUN chown -R appuser:appgroup /app
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
