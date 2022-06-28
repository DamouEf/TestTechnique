FROM python:3.10.2-alpine3.15 

RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt

RUN apk update && apk add  --no-cache postgresql-dev uwsgi uwsgi-python3 gcc python3-dev musl-dev libffi-dev openssl-dev build-base alpine-sdk \
    && pip install --prefix=/install --no-warn-script-location -r /requirements.txt \
    && find /install \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /install \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps


FROM python:3.10.2-alpine3.15
COPY --from=0 /install /usr/local

RUN apk --no-cache add libpq libstdc++ jpeg-dev zlib-dev gcc libgcc linux-headers uwsgi uwsgi-python3 mariadb-dev g++ unixodbc-dev

RUN mkdir /code
COPY . /code/
WORKDIR /code

RUN pip install --upgrade pip

RUN apk --no-cache add libpq libstdc++ make zip uwsgi uwsgi-python3 mariadb-dev musl-dev gcc libgcc

# Install dependencies
RUN apk --no-cache add curl gnupg

# ENV PYTHONPATH=/code
ENV PYTHONUNBUFFERED=0

CMD ["sh", "-c", "tail -f /dev/null"]
