FROM debian:latest

RUN mkdir -p /app/src
COPY ./postgresql-16.2.tar.bz2 /app/src/postgresql-16.2.tar.bz2

RUN apt-get update && \
    apt-get install -y tar bzip2

WORKDIR /app/src
RUN tar xvfj postgresql-16.2.tar.bz2

WORKDIR /app/src/postgresql-16.2
RUN apt-get install -y gcc build-essential pkg-config libicu-dev libreadline-dev lib32z1-dev
RUN ./configure -prefix=/app/pg
RUN make -j $(nproc) && make install

WORKDIR /app/src/postgresql-16.2/contrib
RUN apt-get install -y git
RUN git clone https://github.com/citusdata/citus.git
WORKDIR /app/src/postgresql-16.2/contrib/citus
ENV PATH="/app/pg/bin:${PATH}"
ENV PATH="/app/bin:${PATH}"
RUN apt-get install -y libcurl4-openssl-dev liblz4-dev libzstd-dev
RUN ./configure
RUN make -j $(nproc) && make install

RUN rm -r /app/src

RUN groupadd -r postgres && useradd --no-log-init -r -g postgres -d /app postgres
RUN mkdir -p /app/pgdata
RUN chown -R postgres:postgres /app
WORKDIR /app/pgdata

USER root
RUN apt-get install -y parallel
USER postgres

USER root
run apt-get update
run apt-get install -y python3
run apt-get install -y python3-pip
run apt-get install -y python3-venv
user postgres
workdir /app
run python3 -m venv venv
run . venv/bin/activate && pip install gunicorn flask psycopg2
user root
run apt-get install -y python3-psycopg2

run mkdir -p /app
run chown -R postgres:postgres /app
USER postgres
