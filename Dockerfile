# pull official base image
FROM python:3.8.3-alpine

ENV PATH="/scripts:${PATH}"
#maintainer
LABEL Momodou Krubally "momodou.krubally@axwdigital.fi"
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# copy project



RUN pip install --upgrade pip

RUN apk update && apk add --no-cache \
    postgresql \
    zlib \
    jpeg 

# install dependencies
RUN apk add --no-cache --virtual build-deps \
    gcc \  
    python3-dev \ 
    musl-dev \
    postgresql-dev\
    zlib-dev \
    jpeg-dev \
    libressl-dev \
    libffi-dev 
    


RUN pip3 install setuptools-rust
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt


RUN apk del build-deps && \
    find -type d -name __pycache__ -prune -exec rm -rf {} \; && \
    rm -rf ~/.cache/pip
# removing temporary packages from docker and removing cache 

RUN mkdir /app
COPY ./insightproject /app
WORKDIR /app
COPY ./scripts /scripts

COPY ./insightproject /app

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

#add a nonroot user
RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user

ENTRYPOINT [ "sh", "/scripts/entrypoint.sh" ]
#CMD ["entrypoint.sh"]