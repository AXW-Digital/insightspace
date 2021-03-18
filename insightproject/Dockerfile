# pull official base image
FROM python:3.8


#maintainer
LABEL Momodou Krubally "momodou.krubally@axwdigital.fi"
# set environment variables
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
#working directory
WORKDIR /app

# copy project
COPY . /app

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

