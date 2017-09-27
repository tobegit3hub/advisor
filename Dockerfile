FROM python:2.7

ADD ./requirements.txt /

RUN pip install -r /requirements.txt

ADD . /
WORKDIR /

RUN ./advisor_server/manage.py migrate

EXPOSE 8000

CMD ["./advisor_server/manage.py", "runserver", "0.0.0.0:8000"]
