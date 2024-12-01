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

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./
RUN cd core/

EXPOSE 8000

# CMD ["sh", "-c", "python3 core/manage.py migrate && python3 core/manage.py runserver 0.0.0.0:8000"]

CMD ["python3 manage.py runserver 0.0.0.0:8000"]
