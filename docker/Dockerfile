FROM alpine:latest

MAINTAINER bandbase@jurihock.de

ENV LANG en_US.utf8
ENV PGDATA /bandbase/postgres
ENV PGDATABASE bandbase
ENV PGUSER bandbase

EXPOSE 5432
VOLUME ["/bandbase"]

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

ADD requirements.txt /tmp/requirements.txt

RUN apk update && \
    apk add git postgresql python3 tzdata && \
    rm -rf /var/cache/apk/*

#RUN apk update && \
#    apk add gcc git postgresql postgresql-dev python3 python3-dev texlive texlive-xetex texmf-dist-latexextra ttf-linux-libertine tzdata && \
#    rm -rf /var/cache/apk/*

#RUN python3 -m ensurepip && \
#    pip3 install --upgrade pip setuptools && \
#    pip3 install --requirement /tmp/requirements.txt && \
#    rm -rf /usr/lib/python*/ensurepip && \
#    rm -rf ~/.cache && \
#    if [ ! -e /usr/bin/pip ]; then ln -s $(which pip3) /usr/bin/pip; fi && \
#    if [ ! -e /usr/bin/python ]; then ln -s $(which python3) /usr/bin/python; fi

RUN cp /usr/share/zoneinfo/Europe/Berlin /etc/localtime && \
    echo "Europe/Berlin" > /etc/timezone

RUN wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/1.12/gosu-amd64" && \
    chmod +x /usr/local/bin/gosu

RUN git clone "https://github.com/jurihock/bandbase.git" /bandbase/git
