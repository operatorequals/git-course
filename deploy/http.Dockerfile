# Partially taken from:
# https://linuxhint.com/setup_git_http_server_docker/
FROM ubuntu:18.04

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid
ENV PORT 8000

RUN apt update 2>/dev/null && \
    apt install -y git apache2 apache2-utils python3-pygit2 2>/dev/null && \
    a2enmod env cgi alias rewrite

COPY ./deploy/git.conf /etc/apache2/sites-available/git.conf
COPY ./deploy/ports.conf /etc/apache2/ports.conf

RUN a2dissite 000-default.conf && \
    a2ensite git.conf

RUN git config --system http.receivepack true && \
    git config --system http.uploadpack true

RUN mkdir /var/www/git
ADD --chown=www-data:www-data repos/ var/www/git/
RUN chown -Rfv www-data:www-data /var/www/git
RUN for i in var/www/git/*; do touch $i/git-daemon-export-ok; done

# Template the PORT number for Heroku Runtime
CMD sed -i "s/PORT/$PORT/g" /etc/apache2/sites-available/git.conf && \
    sed -i "s/PORT/$PORT/g" /etc/apache2/ports.conf && \
    /usr/sbin/apache2ctl -D FOREGROUND
EXPOSE 8000
