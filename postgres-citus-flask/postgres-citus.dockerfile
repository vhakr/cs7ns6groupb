FROM debian:latest

RUN apt-get update
RUN apt-get install -y curl vim ssh
RUN apt-get install -y postgresql
RUN service postgresql start
RUN curl https://install.citusdata.com/community/deb.sh | bash
RUN apt-get -y install postgresql-15-citus-11.2
RUN pg_conftool 15 main set shared_preload_libraries citus
RUN pg_conftool 15 main set listen_addresses '*'
RUN update-rc.d postgresql enable
RUN service postgresql restart && su postgres -c "psql -c 'CREATE EXTENSION citus;'"

CMD ["service", "postgresql", "start", ";", "/bin/bash"]
