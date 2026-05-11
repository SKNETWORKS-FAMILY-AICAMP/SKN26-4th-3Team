FROM mysql:8.4.9

COPY conf.d/my.cnf /etc/mysql/conf.d/my.cnf
COPY init/ /docker-entrypoint-initdb.d/

EXPOSE 3306 33060
