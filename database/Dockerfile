FROM mysql:8.4.9

COPY conf.d/my.cnf /etc/mysql/conf.d/my.cnf
COPY init/ /docker-entrypoint-initdb.d/

RUN find /docker-entrypoint-initdb.d -type f -name "*.sh" -exec sed -i 's/\r$//' {} \; \
    -exec chmod +x {} \;

EXPOSE 3306 33060
