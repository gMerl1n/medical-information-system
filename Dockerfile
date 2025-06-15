FROM python:3.10.18-slim

WORKDIR /mis

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn && pip install psycopg2-binary


COPY . .

EXPOSE 8080

RUN chmod a+x ./start.sh

ENTRYPOINT ["./start.sh"]