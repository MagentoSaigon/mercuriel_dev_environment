FROM php:7-apache
RUN \
  apt-get update && \
  apt-get install -y \
  curl \
  wget \
  git \
  vim \
  zip
#  software-properties-common
RUN apt-get update && apt-get install -y \
        libfreetype6-dev \
        libjpeg62-turbo-dev \
        libmcrypt-dev \
        libpng12-dev \
        libxml2-dev \
    && docker-php-ext-install mbstring mcrypt \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install gd \
    && docker-php-ext-configure pdo_mysql --with-pdo-mysql=mysqlnd \
    && docker-php-ext-install pdo_mysql \
    && docker-php-ext-install soap
RUN apt-get update && apt-get install -y \
    php5-cli

RUN yes | pecl install xdebug \
    && echo "zend_extension=$(find /usr/local/lib/php/extensions/ -name xdebug.so)" > /usr/local/etc/php/conf.d/xdebug.ini \
    && echo "xdebug.remote_enable=on" >> /usr/local/etc/php/conf.d/xdebug.ini \
    && echo "xdebug.remote_autostart=off" >> /usr/local/etc/php/conf.d/xdebug.ini \
    && echo "xdebug.remote_log=/var/log/xdebug_remote" >> /usr/local/etc/php/conf.d/xdebug.ini

#RUN rm -rf /var/lib/apt/lists/*
#RUN php5enmod mcrypt
#RUN php5enmod gd
RUN a2enmod rewrite
#RUN service apache2 stop

COPY apache_config /etc/apache2/sites-enabled/000-default.conf

ENV APACHE_RUN_USER=www-data
ENV APACHE_RUN_GROUP=www-data
ENV APACHE_LOG_DIR=/var/log/apache2
ENV APACHE_PID_FILE=/var/run/apache2.pid
#ENV APACHE_RUN_DIR=/var/run/apache2
ENV APACHE_LOCK_DIR=/var/lock/apache2

#ENV APACHE_DOCUMENTROOT=/var/www/html

RUN mkdir -p $APACHE_RUN_DIR $APACHE_LOCK_DIR $APACHE_LOG_DIR

WORKDIR /var/www

CMD ["apache2-foreground"]