FROM python:3.8
WORKDIR /usr/src/SeaWar
RUN pip install --upgrade pip
COPY ./req.txt /usr/src/req.txt
RUN pip install -r /usr/src/req.txt
COPY . .
#COPY ../logs/debug.log /usr/src/logs/debug.log
RUN mkdir /usr/src/logs
CMD touch /usr/src/logs/debug.log
#CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]