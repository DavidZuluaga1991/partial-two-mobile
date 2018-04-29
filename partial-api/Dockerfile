FROM python:3.5

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

COPY . /usr/src/app
COPY partial/.env ./.env
RUN mkdir /usr/src/app/logs

WORKDIR /usr/src/app/partial

CMD [ "python3", "run.py" ]
