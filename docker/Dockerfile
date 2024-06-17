FROM postgres:11.5-alpine

COPY Chinook_PostgreSql.sql /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/Chinook_PostgreSql.sql

