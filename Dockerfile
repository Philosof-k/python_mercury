FROM python:alpine

RUN apk update \
    && apk --no-cache --update add build-base

WORKDIR /usr/src/app

COPY npreal2_v5.1_build_21080410.tgz /tmp
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./bot/bot.py" ]
