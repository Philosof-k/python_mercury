FROM python:3.7-slim

RUN apt-get update && apt-get install build-essential -y

COPY npreal2_v5.1_build_21080410.tgz /tmp
RUN tar -xzvf /tmp/npreal2_v5.1_build_21080410.tgz

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./bot/bot.py" ]
