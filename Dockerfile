FROM python:3.10.15-bullseye

ARG MYSQL_HOST
ARG MYSQL_PORT
ARG MYSQL_ROOT_USER
ARG MYSQL_ROOT_PASSWORD
ARG MYSQL_DB_NAME
ARG SECRET_KEY

ENV MYSQL_HOST=${MYSQL_HOST}
ENV MYSQL_PORT=${MYSQL_PORT}
ENV MYSQL_ROOT_USER=${MYSQL_ROOT_USER}
ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
ENV MYSQL_DB_NAME=${MYSQL_DB_NAME}
ENV SECRET_KEY=${SECRET_KEY}


WORKDIR /app

COPY . /app/


COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
RUN pip install whitenoise

WORKDIR /app/core
RUN python3 manage.py collectstatic 

EXPOSE 8000

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["sh", "-c", "python3 manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3"]