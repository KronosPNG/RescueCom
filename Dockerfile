FROM python:3.14-slim

WORKDIR /app

COPY ./cloud/requirements.txt requirements.txt

RUN python -m pip install --upgrade pip setuptools
RUN python -m pip install -v -r requirements.txt

COPY ./cloud/entrypoint.sh entrypoint.sh
COPY ./cloud ./cloud
COPY ./common ./common

COPY --from=tianon/gosu /gosu /usr/local/bin/

RUN addgroup --gid 1000 appgroup
RUN adduser --gid 1000 --uid 1000 \
			--disabled-password \
			--disabled-login \
			--no-create-home appuser
RUN chown -R appuser:appgroup /app
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cloud:app"]
