FROM php:8.3-apache

ARG MOODLE_VERSION=5.0.2

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        libfreetype6-dev \
        libicu-dev \
        libjpeg62-turbo-dev \
        libpng-dev \
        libxml2-dev \
        libzip-dev \
        unzip \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j"$(nproc)" \
        exif \
        gd \
        intl \
        mysqli \
        opcache \
        soap \
        zip \
    && a2enmod headers rewrite \
    && curl --fail --location --silent --show-error \
        "https://download.moodle.org/download.php/direct/stable500/moodle-${MOODLE_VERSION}.tgz" \
        -o /tmp/moodle.tgz \
    && tar -xzf /tmp/moodle.tgz --strip-components=1 -C /var/www/html \
    && mkdir -p /var/www/moodledata \
    && chown -R www-data:www-data /var/www/html /var/www/moodledata \
    && rm -rf /var/lib/apt/lists/* /tmp/moodle.tgz

COPY docker/php.ini /usr/local/etc/php/conf.d/moodle.ini

WORKDIR /var/www/html

EXPOSE 80
