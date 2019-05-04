FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev \
  tk-dev tcl-dev


COPY ./requirements.txt /requirements/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /requirements/requirements.txt \
    && rm -rf /requirements

COPY ./start /start


RUN addgroup -S django \
    && adduser -S -G django django \
    && sed -i 's/\r//' /start \
    && chmod +x /start \
    && chown django /start

COPY . /app

RUN mkdir /var/log/app/ && chown -R django /app /var/log/app/

USER django

WORKDIR /app

ENTRYPOINT ["/start"]
