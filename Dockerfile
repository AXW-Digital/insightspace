# pull official base image
FROM python:3.8 

ENV PATH="/scripts:${PATH}"
#maintainer
LABEL Momodou Krubally "momodou.krubally@axwdigital.fi"
# set environment variables
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
#working directory
WORKDIR /app

# copy project
COPY ./insightproject /app

COPY ./scripts /scripts

RUN chmod +x /scripts/*
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user


# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["entrypoint.sh"]

