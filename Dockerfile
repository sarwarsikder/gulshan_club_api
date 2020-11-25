FROM python:3.7-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add \
    bash \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    harfbuzz-dev \
    fribidi-dev \
    py3-magic \
  && rm -rf /var/cache/apk/*

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN python -m pip install -r requirements.txt

COPY . .

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

