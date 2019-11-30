FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /

COPY . .

RUN mkdir ./torrents

CMD [ "python", "./auto-linux-watcher.py" ]
